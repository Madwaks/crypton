from logging import getLogger
from typing import List, NoReturn, Union

from django.db.models import QuerySet
from injector import singleton, inject
from pandas import DataFrame
from tqdm import tqdm

from crypto.models import Symbol, Quote
from decision_maker.models import Indicator, SymbolIndicator
from decision_maker.models.distance import Distance
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
        quotes_for_symbol_and_tu = symbol.quotes.get_symbol_and_tu_quotes(
            time_unit=time_unit
        )
        quotes_for_symbol_and_tu
        self._compute_symbol_indicators(symbol, time_unit, quotes_for_symbol_and_tu)
        #
        self._compute_quote_indicators(symbol, quotes_for_symbol_and_tu)

        self._compute_quote_to_ind_distances(quotes_for_symbol_and_tu)

        # self._compute_distances_for_symbol(symbol)

    def _compute_quote_to_ind_distances(
        self, quotes_for_symbol_and_tu: QuerySet[Quote]
    ) -> NoReturn:
        distances = []
        for quote in tqdm(quotes_for_symbol_and_tu.prefetch_related("indicators")):
            res, supp = quote.nearest_key_level

            mm7 = quote.indicators.get(name="MM7")
            mm20 = quote.indicators.get(name="MM20")
            mm50 = quote.indicators.get(name="MM50")
            mm100 = quote.indicators.get(name="MM100")
            mm200 = quote.indicators.get(name="MM200")

            distance = Distance()

            if mm7.value != 0:
                distance.mm7 = (mm7.value - quote.close) / quote.close
            if mm20.value != 0:
                distance.mm20 = (mm20.value - quote.close) / quote.close
            if mm50.value != 0:
                distance.mm50 = (mm50.value - quote.close) / quote.close
            if mm100.value != 0:
                distance.mm100 = (mm100.value - quote.close) / quote.close
            if mm200.value != 0:
                distance.mm200 = (mm200.value - quote.close) / quote.close
            distance.support = (supp - quote.close) / quote.close
            distance.resistance = (res - quote.close) / quote.close
            distance.quote = quote
            distances.append(distance)
        Distance.objects.bulk_create(distances)

    def _compute_symbol_indicators(
        self,
        symbol: Union[str, Symbol],
        time_unit: TimeUnits,
        quotes_for_symbol_and_tu: QuerySet[Quote],
    ) -> NoReturn:
        symbol_indicators = self._key_level_factory.build_key_level_for_symbol(
            symbol, time_unit, quotes_for_symbol_and_tu
        )
        SymbolIndicator.objects.filter(symbol=symbol, time_unit=time_unit).delete()

        self._save_symbol_indicators(symbol_indicators)

    def _compute_quote_indicators(
        self, symbol: Union[str, Symbol], quotes_for_symbol_and_tu: QuerySet[Quote]
    ) -> NoReturn:
        quote_as_dataframe: DataFrame = DataFrame(
            list(quotes_for_symbol_and_tu.values())
        )
        if not quote_as_dataframe.empty:
            indicators = self._indicators_factory.build_indicators_from_dataframe(
                quote_as_dataframe, symbol
            )
            self._save_indicators(indicators)
        else:
            logger.warning(f"No quotes saved for {symbol}. Run importquotes command.")

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
