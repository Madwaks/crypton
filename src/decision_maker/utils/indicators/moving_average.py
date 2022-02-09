import itertools
from typing import NoReturn, Optional

from django.db.models import QuerySet
from injector import singleton
from pandas import Series, DataFrame

from crypto.models import Quote
from decision_maker.models import Indicator


@singleton
class MovingAverageIndicatorFactory:
    new_indicators_name: set = set()
    periods: list[int] = [7, 20, 50, 100, 200]

    def build_moving_average_indicators(self, quotes: QuerySet[Quote]):
        dataframe: DataFrame = DataFrame(list(quotes.values()))
        moving_avg_dataframe = self._build_moving_average_df(dataframe)

        timestamp_miss_indicators = quotes.filter(indicators__isnull=True)
        return (
            self._build_indicators(timestamp_miss_indicators, moving_avg_dataframe)
            or []
        )

    def _build_indicators(
        self, missing_quotes: QuerySet[Quote], mov_avg_df: DataFrame
    ) -> Optional[list[Indicator]]:
        mov_avg_df = mov_avg_df[
            mov_avg_df["close_time"].isin(
                missing_quotes.values_list("close_time", flat=True)
            )
        ]
        if not mov_avg_df.empty:
            indicators = (
                mov_avg_df.fillna(0)
                .apply(self._parse_row_into_indicator, axis=1, args=(missing_quotes,))
                .dropna()
                .to_list()
            )
            return list(itertools.chain.from_iterable(indicators))

    def _build_moving_average_df(self, quotes_as_df: DataFrame) -> DataFrame:
        indicators_df = quotes_as_df[["timestamp", "close_time"]].copy()
        for period in self.periods:
            mm: Series = simple_moving_average(quotes_as_df, period=period)
            self.new_indicators_name.add(mm.name)
            indicators_df[mm.name] = mm
        return indicators_df

    def _parse_row_into_indicator(self, row, quotes):
        quote = quotes.get(timestamp=row["timestamp"])
        indicators = []
        for indicator_name in self.new_indicators_name:
            ind_val = row[indicator_name]
            indicators.append(
                Indicator(name=indicator_name, value=ind_val, quote=quote)
            )
        return indicators


def exp_moving_average(quotes: DataFrame, period: int) -> Series:
    quotation_series: Series = Series(data=quotes.close, index=quotes.index)
    return quotation_series.ewm(span=period, adjust=False).mean()


def simple_moving_average(quotes: DataFrame, period: int) -> Series:
    quotation_series = Series(data=quotes.close, index=quotes.index)
    rolling_mean_name = f"MM{period}"
    mm = quotation_series.rolling(window=period).mean()
    mm.name = rolling_mean_name
    return mm


def macd(quotes: DataFrame) -> NoReturn:
    macd_hist = exp_moving_average(quotes, 26) - exp_moving_average(quotes, 12)
    quotes["macd_hist"] = macd_hist


def macd_signal(macd_hist: Series) -> NoReturn:
    mme9 = macd_hist.ewm(span=9, adjust=False).mean()
    mme9.name = "MME9"
    return mme9
