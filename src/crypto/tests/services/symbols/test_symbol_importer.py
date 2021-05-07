import pytest

from crypto.models import Symbol
from crypto.services.importers.symbol import SymbolImporter


@pytest.mark.django_db
def test_symbol_importer(symbol_importer: SymbolImporter):
    symbol_importer.import_all_symbols()
    symbols = Symbol.objects.all()
    symbol_names = [symb.name for symb in symbols]
    assert str(symbols[0]) == symbols[0].name
    assert len(symbols) == 4
    assert "ETHBTC" in symbol_names
