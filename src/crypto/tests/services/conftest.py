from pathlib import Path

import pytest

from crypto.services.repositories.pair import SymbolRepository
from utils.enums import TimeUnits
from utils.service_provider import build


@pytest.fixture(scope="module")
def time_unit_4h() -> TimeUnits:
    return TimeUnits.from_code("4h")


@pytest.fixture(scope="module")
def time_unit_1d() -> TimeUnits:
    return TimeUnits.from_code("1d")


@pytest.fixture(scope="module")
def symbol_json_path() -> Path:
    return Path("crypto/tests/data/mock_symbols.json")


@pytest.fixture(scope="module")
def symbol_repository_config(symbol_json_path: Path) -> SymbolRepository.Configuration:
    return SymbolRepository.Configuration(symbol_json_file=symbol_json_path)


@pytest.fixture(scope="module")
def symbol_repository(
    symbol_repository_config: SymbolRepository.Configuration,
) -> SymbolRepository:
    return build(SymbolRepository, config=symbol_repository_config)
