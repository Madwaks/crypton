from datetime import datetime, timedelta

from dateutil import tz

from crypto.models import Symbol
from crypto.utils.most_traded_coins import MOST_TRADED_COINS, MOST_VARIANCE_COINS
from utils.enums import TimeUnits

SYMBOLS_TO_COMPUTE = Symbol.objects.filter(name__in=MOST_VARIANCE_COINS)


def is_quote_uncomplete(obj: dict, time_unit: TimeUnits):
    return open_date(obj) < close_date(obj) - (
        time_unit.to_timedelta() - timedelta(minutes=2)
    )


def open_date(quote):
    if isinstance(quote, int):
        dt = datetime.fromtimestamp(int(quote), tz=tz.tzutc())
    else:
        dt = datetime.fromtimestamp(int(quote.get("timestamp")), tz=tz.tzutc())
    return datetime(
        year=dt.year,
        month=dt.month,
        day=dt.day,
        hour=dt.hour,
        minute=dt.minute,
        second=dt.second,
    )


def close_date(quote):
    if isinstance(quote, int):
        dt = datetime.fromtimestamp(int(quote), tz=tz.tzutc())
    else:
        dt = datetime.fromtimestamp(int(quote.get("timestamp")), tz=tz.tzutc())
    return datetime(
        year=dt.year,
        month=dt.month,
        day=dt.day,
        hour=dt.hour,
        minute=dt.minute,
        second=dt.second,
    )
