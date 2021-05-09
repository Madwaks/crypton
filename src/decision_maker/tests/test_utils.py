from datetime import datetime, timedelta

import pytest
from pytest_factoryboy import register

from crypto.models import Quote
from crypto.tests.factories.quote import QuotesFactory
from decision_maker.utils.etc import get_timestamp_diff_unit

register(QuotesFactory)


@pytest.mark.django_db
@pytest.mark.parametrize("quote__time_unit", ["1m", "5m", "15m", "30m"])
@pytest.mark.parametrize("diff_number", [2, 3, 10, 20, 4, 5, 50, 100, 125, 200])
def test_get_timestamp_diff_unit_minutes(quote: Quote, diff_number: int):
    ts = get_timestamp_diff_unit(quote, diff_number)
    dt = datetime.fromtimestamp(ts)
    assert dt == quote.open_date - timedelta(
        minutes=diff_number * int(quote.time_unit.split("m")[0])
    )


@pytest.mark.django_db
@pytest.mark.parametrize("quote__time_unit", ["1h", "4h"])
@pytest.mark.parametrize("diff_number", [2, 3, 10, 20, 4, 5, 50, 100, 125, 200])
def test_get_timestamp_diff_unit_hours(quote: Quote, diff_number: int):
    ts = get_timestamp_diff_unit(quote, diff_number)
    dt = datetime.fromtimestamp(ts)
    assert dt == quote.open_date - timedelta(
        hours=diff_number * int(quote.time_unit.split("h")[0])
    )


@pytest.mark.django_db
@pytest.mark.parametrize("quote__time_unit", ["1d"])
@pytest.mark.parametrize("diff_number", [2, 3, 10, 20, 4, 5, 50, 100, 125, 200])
def test_get_timestamp_diff_unit_days(quote: Quote, diff_number: int):
    ts = get_timestamp_diff_unit(quote, diff_number)
    dt = datetime.fromtimestamp(ts)
    assert dt == quote.open_date - timedelta(
        days=diff_number * int(quote.time_unit.split("d")[0])
    )


@pytest.mark.django_db
@pytest.mark.parametrize("quote__time_unit", ["1w"])
@pytest.mark.parametrize("diff_number", [2, 3, 10, 20, 4, 5, 50, 100, 125, 200])
def test_get_timestamp_diff_unit_weeks(quote: Quote, diff_number: int):
    ts = get_timestamp_diff_unit(quote, diff_number)
    dt = datetime.fromtimestamp(ts)
    assert dt == quote.open_date - timedelta(
        weeks=diff_number * int(quote.time_unit.split("w")[0])
    )
