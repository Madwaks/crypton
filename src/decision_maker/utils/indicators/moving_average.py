from typing import NoReturn

from pandas import Series, DataFrame


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
