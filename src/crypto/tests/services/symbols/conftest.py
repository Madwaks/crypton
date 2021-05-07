from pathlib import Path
from typing import NoReturn

import pytest

from crypto.services.importers.symbol import SymbolImporter
from utils.service_provider import provide


class _MockSymbolImporter(SymbolImporter):
    @property
    def json_file_path(self):
        return Path("crypto/tests/data/mock_symbols.json")

    def _download_available_pairs(self) -> NoReturn:
        pass


@pytest.fixture(scope="module")
def symbol_importer() -> SymbolImporter:
    return provide(_MockSymbolImporter)
