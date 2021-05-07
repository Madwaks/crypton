from crypto.services.repositories.pair import SymbolRepository


def test_get_symbols(symbol_repository: SymbolRepository):
    symbols = symbol_repository.get_symbols_from_file()
    assert len(symbols) == 4
