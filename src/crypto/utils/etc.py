from datetime import datetime


def open_date(quote):
    dt = datetime.fromtimestamp(int(quote.get("timestamp")) / 1000)
    return datetime(
        year=dt.year,
        month=dt.month,
        day=dt.day,
        hour=dt.hour,
        minute=dt.minute,
        second=dt.second,
    )


def close_date(quote):
    dt = datetime.fromtimestamp(int(quote.get("close_time")) / 1000)
    return datetime(
        year=dt.year,
        month=dt.month,
        day=dt.day,
        hour=dt.hour,
        minute=dt.minute,
        second=dt.second,
    )