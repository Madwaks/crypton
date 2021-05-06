from datetime import datetime

import pytest
from pytest_factoryboy import register

from crypto.models import Quote
from crypto.tests.factories.quote import QuotesFactory
from crypto.tests.factories.symbol import SymbolFactory

register(SymbolFactory)
register(QuotesFactory)


@pytest.mark.django_db
def test_quote(quote: Quote):
    assert quote.symbol
    assert quote.open_date > datetime(year=1970, month=1, day=1)
    assert quote.close_date < datetime(year=3000, month=1, day=1)
