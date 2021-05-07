from pathlib import Path

from pytest_factoryboy import register

from crypto.models import Symbol
from crypto.services.repositories.quote import QuotesPairRepository
from crypto.tests.factories.symbol import SymbolFactory
from utils.enums import TimeUnits

register(SymbolFactory)


def test_quotes_json_path(
    quote_repository: QuotesPairRepository,
    symbol: Symbol,
    time_unit_1d: TimeUnits,
    mock_quote_json_folder: Path,
):
    assert (
        quote_repository.get_json_path_for_symbol(symbol, time_unit_1d)
        == mock_quote_json_folder / f"{symbol.name}-{time_unit_1d.value}-data.json"
    )


def test_build_file_name(
    quote_repository: QuotesPairRepository, symbol: Symbol, time_unit_1d: TimeUnits
):
    assert (
        quote_repository._build_file_name(symbol, time_unit_1d)
        == f"{symbol.name}-{time_unit_1d.value}-data"
    )
