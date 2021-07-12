from logging import getLogger
from typing import List, NoReturn, Union

from injector import singleton, inject
from pandas import DataFrame

from crypto.models import Symbol
from decision_maker.models import Indicator, SymbolIndicator
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

        self._compute_symbol_indicators(symbol, time_unit)

        self._compute_quote_indicators(symbol, time_unit)
        #
        # self._compute_distances_for_symbol(symbol)

    def _compute_symbol_indicators(
        self, symbol: Union[str, Symbol], time_unit: TimeUnits
    ) -> NoReturn:
        symbol_indicators = self._key_level_factory.build_key_level_for_symbol(
            symbol, time_unit=time_unit
        )
        SymbolIndicator.objects.filter(symbol=symbol, time_unit=time_unit).delete()
        assert (
            len(SymbolIndicator.objects.filter(symbol=symbol, time_unit=time_unit)) == 0
        )
        self._save_symbol_indicators(symbol_indicators)
        assert len(
            SymbolIndicator.objects.filter(symbol=symbol, time_unit=time_unit)
        ) == len(symbol_indicators)

    def _compute_quote_indicators(
        self, symbol: Union[str, Symbol], time_unit: TimeUnits
    ) -> NoReturn:
        quote_as_dataframe: DataFrame = symbol.quotes.get_as_dataframe(
            time_unit=time_unit
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
