from logging import getLogger
from typing import List, NoReturn, Union

from injector import singleton, inject
from pandas import DataFrame
from tqdm import tqdm

from crypto.models import Symbol
from decision_maker.models import Indicator, SymbolIndicator
from decision_maker.services.factories.indicators import DataFrameIndicatorFactory
from decision_maker.services.factories.key_level import KeyLevelFactory
from utils.enums import TimeUnits

logger = getLogger("django")


@singleton
class IndicatorComputer:
    @inject
    def __init__(
        self,
        indicators_factory: DataFrameIndicatorFactory,
        key_levels_factory: KeyLevelFactory,
    ):
        self._indicators_factory = indicators_factory
        self._key_level_factory = key_levels_factory

    def compute_indicators_for_all(self):
        for symbol in tqdm(Symbol.objects.all()):
            self._compute_indicators_for_symbol(symbol)

    def compute_indicators_for_symbol(
        self, symbol: Union[str, Symbol], time_unit: TimeUnits
    ) -> NoReturn:
        if isinstance(symbol, str):
            symbol = Symbol.objects.get(name=symbol)

        symbol_indicators = self._key_level_factory.build_key_level_for_symbol(
            symbol, time_unit=time_unit
        )
        self._save_symbol_indicators(symbol_indicators)

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

    @staticmethod
    def _save_indicators(indicator_list: List[Indicator]) -> NoReturn:
        Indicator.objects.bulk_create(indicator_list)
        logger.info(
            f"[Indicators] Stored {len(indicator_list)} indicator values for {set([ind.name for ind in indicator_list])}"
        )

    @staticmethod
    def _save_symbol_indicators(indicator_list: List[SymbolIndicator]) -> NoReturn:
        SymbolIndicator.objects.bulk_create(indicator_list)
        logger.info(
            f"[Indicators] Stored {len(indicator_list)} indicator values for {set([ind.name for ind in indicator_list])}"
        )
