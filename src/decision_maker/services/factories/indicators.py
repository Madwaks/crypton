from typing import List

from injector import singleton
from pandas import DataFrame, Series

from crypto.models import Quote, Symbol
from decision_maker.models import Indicator
from decision_maker.utils.indicators.moving_average import simple_moving_average


@singleton
class DataFrameIndicatorFactory:
    new_indicators_name: set = set()

    def build_indicators_from_dataframe(
        self, quotes_as_dataframe: DataFrame, symbol: Symbol
    ) -> List[Indicator]:
        indicators_dataframe = self._build_dataframe(quotes_as_dataframe)
        return self._build_indicators(indicators_dataframe, symbol=symbol)

    def _build_dataframe(self, quotes_as_dataframe: DataFrame) -> DataFrame:
        moving_avg_df = self._build_moving_average_df(quotes_as_dataframe)

        return moving_avg_df

    def _build_moving_average_df(self, quotes_as_df: DataFrame) -> DataFrame:
        indicators_df = quotes_as_df.copy()
        for period in [7, 20, 50, 100, 200]:
            mm: Series = simple_moving_average(quotes_as_df, period=period)
            self.new_indicators_name.add(mm.name)
            indicators_df[mm.name] = mm
        return indicators_df

    def _build_indicators(
        self, quotes_as_dataframe: DataFrame, symbol: Symbol
    ) -> List[Indicator]:
        list_indicators = []
        quotes = Quote.objects.filter(symbol=symbol)
        for i, row in quotes_as_dataframe.fillna(0).iterrows():
            quote = quotes.get(timestamp=row["timestamp"])
            for indicator_name in self.new_indicators_name:
                ind_val = row[indicator_name]
                if (
                    quote.indicators.filter(name=indicator_name).exists()
                    or ind_val == 0
                ):
                    continue
                list_indicators.append(
                    Indicator(name=indicator_name, value=ind_val, quote=quote)
                )

        return list_indicators
