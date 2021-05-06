import pytest
from pytest_factoryboy import register

from crypto.models import Symbol
from crypto.tests.factories.quote import QuotesFactory
from crypto.tests.factories.symbol import SymbolFactory

register(SymbolFactory)
register(QuotesFactory)


@pytest.mark.django_db
def test_symbol(symbol: Symbol):
    assert str(symbol) == symbol.name
