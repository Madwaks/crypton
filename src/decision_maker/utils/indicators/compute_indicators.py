from logging import getLogger
from typing import List, NoReturn, Union

from django.db.models import QuerySet
from injector import singleton, inject
from pandas import DataFrame
from tqdm import tqdm

from crypto.models import Symbol, Quote
from decision_maker.models import Indicator, SymbolIndicator
from decision_maker.models.distance import Distance
from decision_maker.models.enums import AvailableIndicators
from decision_maker.models.quote_state import QuoteState
from decision_maker.services.factories.indicators import DataFrameIndicatorFactory
from decision_maker.services.factories.key_level import KeyLevelFactory
from decision_maker.services.factories.quote_state import QuoteStateFactory
from utils.enums import TimeUnits

logger = getLogger("django")


@singleton
class IndicatorComputer:
    @inject
    def __init__(
        self,
        indicators_factory: DataFrameIndicatorFactory,
        key_levels_factory: KeyLevelFactory,
        distance_factory: QuoteStateFactory,
    ):
        self._indicators_factory = indicators_factory
        self._key_level_factory = key_levels_factory
        self._distance_factory = distance_factory

    def compute_indicators_for_symbol(
        self, symbol: Union[str, Symbol], time_unit: TimeUnits
    ) -> NoReturn:
        if isinstance(symbol, str):
            symbol = Symbol.objects.get(name=symbol)
        quotes = symbol.quotes.get_symbol_and_tu_quotes(time_unit=time_unit)

        if symbol.quotes.exists() or quotes.exists():
            if not symbol.indicators.exists():
                self._compute_symbol_indicators(symbol, time_unit, quotes)

            quotes_with_missing_indicators = quotes.filter(indicators=None)

            self._compute_quote_indicators(symbol, quotes_with_missing_indicators)
            quote_without_distances = quotes.filter(distances=None)
            self._compute_quote_to_ind_distances(quote_without_distances)

            # self._compute_distances_for_symbol(symbol)

    def _compute_quote_to_ind_distances(self, quotes: QuerySet[Quote]) -> NoReturn:
        distances = []
        available_indicators = AvailableIndicators.values
        for quote in tqdm(quotes.prefetch_related("indicators")):
            distance = Distance(quote=quote)
            res, supp = quote.nearest_key_level

            for indicator_name in available_indicators:
                mm = quote.indicators.get(name=indicator_name.upper())
                if mm.value != 0:
                    setattr(
                        distance,
                        indicator_name.upper(),
                        (quote.close - mm.value) / quote.close,
                    )

            distance.support = (quote.close - supp) / quote.close
            distance.resistance = (quote.close - res) / quote.close

            distances.append(distance)

        Distance.objects.bulk_create(distances)

    def _compute_symbol_indicators(
        self, symbol: Union[str, Symbol], time_unit: TimeUnits, quotes: QuerySet[Quote]
    ) -> NoReturn:
        symbol_indicators = self._key_level_factory.build_key_level_for_symbol(
            symbol, time_unit, quotes
        )
        SymbolIndicator.objects.filter(symbol=symbol, time_unit=time_unit).delete()

        self._save_symbol_indicators(symbol_indicators)

    def _compute_quote_indicators(
        self, symbol: Union[str, Symbol], quotes: QuerySet[Quote]
    ) -> NoReturn:
        dataframe: DataFrame = DataFrame(list(quotes.values()))
        if not dataframe.empty:
            indicators = self._indicators_factory.build_indicators_from_dataframe(
                dataframe, symbol
            )
            self._save_indicators(indicators)

    def _compute_distances_for_symbol(self, symbol: Symbol):
        if isinstance(symbol, str):
            symbol = Symbol.objects.get(name=symbol)

        quote_states = self._distance_factory.build_states_from_quotes(
            symbol.quotes.all()
        )
        self.save_states(quote_states)

    @staticmethod
    def save_states(quote_list: list[QuoteState]):

        try:
            QuoteState.objects.bulk_create(quote_list)
        except:
            logger.info("[Distances] Some distances are already known, trying 1by1...")
            for quote_state in quote_list:
                try:
                    quote_state.save()
                except:
                    continue

        logger.info(f"[Distances] Stored {len(quote_list)} quote states")

    @staticmethod
    def _save_indicators(indicator_list: List[Indicator]) -> NoReturn:
        try:
            Indicator.objects.bulk_create(indicator_list)
        except:
            logger.info(
                "[Indicators] Some indicators are already known, trying 1by1..."
            )
            for indicator in indicator_list:
                try:
                    indicator.save()
                except:
                    continue
        logger.info(
            f"[Indicators] Stored {len(indicator_list)} indicator values for {set([ind.name for ind in indicator_list])}"
        )

    @staticmethod
    def _save_symbol_indicators(indicator_list: List[SymbolIndicator]) -> NoReturn:
        try:
            SymbolIndicator.objects.bulk_create(indicator_list)
        except:
            logger.info(
                "[Indicators] Some indicators are already known, trying 1by1..."
            )
            for indicator in indicator_list:
                try:
                    indicator.save()
                except:
                    continue
        logger.info(
            f"[Indicators] Stored {len(indicator_list)} indicator values for {set([ind.name for ind in indicator_list])}"
        )
