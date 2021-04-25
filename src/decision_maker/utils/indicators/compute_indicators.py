from logging import getLogger
from typing import List, NoReturn

from injector import singleton, inject
from pandas import DataFrame
from tqdm import tqdm

from crypto.models import Symbol
from decision_maker.models import Indicator
from decision_maker.services.factories.indicators import DataFrameIndicatorFactory

logger = getLogger()


@singleton
class IndicatorComputer:
    @inject
    def __init__(self, indicators_factory: DataFrameIndicatorFactory):
        self._indicators_factory = indicators_factory

    def compute_indicators_for_all(self):
        for symbol in tqdm(Symbol.objects.all()):
            self._compute_indicators_for_symbol(symbol)

    def _compute_indicators_for_symbol(self, symbol: Symbol) -> NoReturn:
        quote_as_dataframe: DataFrame = symbol.quotes.get_as_dataframe()
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
