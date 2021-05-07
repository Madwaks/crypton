from datetime import datetime

import pytest
from pytest_factoryboy import register

from crypto.models import Symbol, Quote
from crypto.services.importers.quotes import QuotesPairImporter
from crypto.tests.factories.symbol import SymbolFactory
from utils.enums import TimeUnits

register(SymbolFactory, name="ETHBTC")


@pytest.mark.django_db
def test_quote_importer(
    quote_importer: QuotesPairImporter, symbol: Symbol, time_unit_1d: TimeUnits
):
    symbol.save()
    quote_importer.import_quotes(symbol=symbol, time_unit=time_unit_1d)
    assert len(Quote.objects.all()) == 12
    assert len(Quote.objects.order_by("symbol__name").distinct("symbol__name")) == 1

    quote = Quote.objects.first()

    assert quote.symbol == symbol
    assert quote.open_date >= datetime(2017, 1, 1, 0, 0)
