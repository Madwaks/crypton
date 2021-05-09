import datetime
from statistics import mean
from typing import Type, List, Optional

from django.db.models import QuerySet
from pandas.tseries.offsets import BDay

from crypto.models import Quote
from decision_maker.models import Indicator
from utils.enums import TimeUnits


def get_quotations_range(quotation: Quote, date_range: List["datetime"]) -> QuerySet:

    return Quote.objects.filter(date__range=date_range, company=quotation.symbol)


def _get_date_range(date: Type["datetime"], period: int) -> List[Type["datetime"]]:
    n_days_before = date - BDay(period - 1)
    return [
        datetime.date(
            year=n_days_before.year, month=n_days_before.month, day=n_days_before.day
        ),
        date,
    ]


def get_mean_highest_lowest(quotation_values: QuerySet):
    last_values = [
        [quot.close, quot.high, quot.low, quot.open] for quot in quotation_values
    ]
    max_ = max([max(value) for value in last_values])
    min_ = min([min(value) for value in last_values])
    return (max_ + min_) / 2


def compute_tenkan(quotation: Quote, period: Optional[int] = 9) -> Optional[float]:
    last_nine_quotation = get_quotations_range(
        quotation, _get_date_range(quotation.date, period=period)
    )
    return get_mean_highest_lowest(last_nine_quotation)


def compute_kijun(quotation: Quote, period: Optional[int] = 26) -> Optional[float]:
    last_quotations = get_quotations_range(
        quotation, _get_date_range(quotation.date, period=period)
    )
    return get_mean_highest_lowest(quotation_values=last_quotations)


def compute_chikou(quotation: Quote) -> Optional[float]:
    day_before = 26

    date = quotation.date + BDay(day_before)
    while date not in [
        quot.date for quot in Quote.objects.filter(company=quotation.company)
    ]:
        date = quotation.date - BDay(day_before + 1)
        day_before = day_before + 1
        if date < quotation.date + BDay(30):
            return None
    quot = Quote.objects.get(date=date, company=quotation.company)

    return quot.close if quot else None


def compute_senko_a(quotation: Quote):
    day_before = 26

    date = quotation.date - BDay(26)

    while date not in [
        quot.date for quot in Quote.objects.filter(company=quotation.company)
    ]:
        date = quotation.date - BDay(day_before - 1)
        day_before = day_before - 1
        if date < quotation.date - BDay(30):
            return None

    early_quotation = Quote.objects.get(date=date, company=quotation.company)
    if early_quotation.indicator:
        tenkan = early_quotation.indicator.get(name="tenkan").value
        kijun = early_quotation.indicator.get(name="kijun").value
        return (tenkan + kijun) / 2 if tenkan and kijun else None


def compute_senko_b(quotation: Quote):
    day_before = 26

    date = quotation.date - BDay(day_before)

    while date not in [
        quot.date for quot in Quote.objects.filter(company=quotation.company)
    ]:
        date = quotation.date - BDay(day_before - 1)
        day_before = day_before - 1
        if date < date - BDay(30):
            return None

    early_quotation = Quote.objects.get(date=date, company=quotation.company)
    return compute_kijun(early_quotation, period=52)


def compute_moving_average(quotation: Quote, period: int) -> Optional[float]:
    quotations = get_quotations_range(
        quotation=quotation, date_range=_get_date_range(quotation.date, period)
    )
    close = [quot.close for quot in quotations]
    return mean(close)


def _compute_indicators(quote: Quote):  # noqa: C901
    if not quote.indicator.filter(name="tenkan"):
        Indicator(quotation=quote, name="tenkan", value=compute_tenkan(quote)).save()

    if not quote.indicator.filter(name="kijun"):
        Indicator(quotation=quote, name="kijun", value=compute_kijun(quote)).save()

    if not quote.indicator.filter(name="chiko"):
        Indicator(quotation=quote, name="chiko", value=compute_chikou(quote)).save()

    if not quote.indicator.filter(name="senko_a"):
        Indicator(quotation=quote, name="senko_a", value=compute_senko_a(quote)).save()

    if not quote.indicator.filter(name="senko_b"):
        Indicator(quotation=quote, name="senko_b", value=compute_senko_b(quote)).save()

    if not quote.indicator.filter(name="mm_7"):
        Indicator(
            quotation=quote, name="mm_7", value=compute_moving_average(quote, period=7)
        ).save()

    if not quote.indicator.filter(name="mm_20"):
        Indicator(
            quotation=quote,
            name="mm_20",
            value=compute_moving_average(quote, period=20),
        ).save()

    if not quote.indicator.filter(name="mm_50"):
        Indicator(
            quotation=quote,
            name="mm_50",
            value=compute_moving_average(quote, period=50),
        ).save()

    if not quote.indicator.filter(name="mm_100"):
        Indicator(
            quotation=quote,
            name="mm_100",
            value=compute_moving_average(quote, period=100),
        ).save()

    if not quote.indicator.filter(name="mm_200"):
        Indicator(
            quotation=quote,
            name="mm_200",
            value=compute_moving_average(quote, period=200),
        ).save()


def get_timestamp_diff_unit(
    quote: Quote, diff_number: int
) -> datetime.datetime.timestamp:
    time_unit = TimeUnits.from_code(quote.time_unit)
    return int(
        datetime.datetime.timestamp(
            quote.open_date - diff_number * time_unit.to_timedelta()
        )
    )
