import pytest
from pandas import DataFrame
from pytest_factoryboy import register

from crypto.models import Quote
from crypto.tests.factories.quote import QuotesFactory

register(QuotesFactory, timestamp="12367", time_unit="1d")


@pytest.mark.django_db
def test_quote_as_dataframe(quote: Quote):
    quote.save()

    df = Quote.objects.get_as_dataframe(symbol=quote.symbol, time_unit=quote.time_unit)
    assert isinstance(df, DataFrame)
    assert len(df) == 1
    assert all(
        field
        for field in [
            "timestamp",
            "close",
            "open",
            "high",
            "low",
            "volume",
            "close_time",
        ]
    )
