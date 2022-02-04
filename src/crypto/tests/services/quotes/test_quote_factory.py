import datetime
from typing import Any

import pytest
from pytest_factoryboy import register

from crypto.models import Symbol
from crypto.services.factories.quote import QuoteFactory
from crypto.tests.factories.quote import QuotesFactory
from crypto.tests.factories.symbol import SymbolFactory
from utils.enums import TimeUnits

register(QuotesFactory)
register(SymbolFactory)


@pytest.mark.django_db
def test_build_simple_quote(
    mock_quote_factory: QuoteFactory,
    mock_quotes_json: list[dict[str, Any]],
    symbol: Symbol,
    time_unit_4h: TimeUnits,
):
    quotes = mock_quote_factory.build_quote_for_symbol(
        objs=mock_quotes_json, symbol=symbol, time_unit=time_unit_4h
    )
    quote = quotes[0]

    assert str(quote) == f"{quote.symbol.name} - {quote.open_date} - {quote.time_unit}"
    assert quote.timestamp == "1500004800000"
    assert quote.open == 0.08
    assert quote.close == 0.088591
    assert quote.high == 0.088669
    assert quote.low == 0.08
    assert quote.symbol == symbol
    assert quote.volume == 646.15
    assert quote.close_time == "1500019199999"
    assert quote.open_date == datetime.datetime(2017, 7, 14, 4, 0)
    assert quote.close_date == datetime.datetime(2017, 7, 14, 7, 59, 59, 999000)
