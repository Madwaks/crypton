import json
from pathlib import Path
from typing import NoReturn, Any

import pytest

from crypto.services.importers.symbol import SymbolImporter
from crypto.services.factories.symbol import SymbolFactory
from utils.service_provider import provide


class _MockSymbolImporter(SymbolImporter):
    @property
    def json_file_path(self):
        return Path("crypto/tests/data/mock_symbols.json")

    def _download_available_pairs(self) -> NoReturn:
        pass


@pytest.fixture(scope="module")
def mock_symbols_json(symbol_json_path: Path) -> list[dict[str, Any]]:
    return json.loads(symbol_json_path.read_text())


@pytest.fixture(scope="module")
def symbol_importer() -> SymbolImporter:
    return provide(_MockSymbolImporter)


@pytest.fixture(scope="module")
def symbol_factory() -> SymbolFactory:
    return provide(SymbolFactory)
