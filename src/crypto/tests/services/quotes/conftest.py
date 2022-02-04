import json
from pathlib import Path
from typing import Any

import pytest

from crypto.services.factories.quote import QuoteFactory
from crypto.services.importers.quotes import QuoteImporter
from crypto.services.repositories.quote import QuotesPairRepository
from utils.service_provider import provide, build


@pytest.fixture(scope="module")
def mock_quote_factory() -> QuoteFactory:
    return provide(QuoteFactory)


@pytest.fixture(scope="module")
def mock_quotes_json(path_to_quotes: Path) -> list[dict[str, Any]]:
    return json.loads(path_to_quotes.read_text())


@pytest.fixture(scope="module")
def path_to_quotes() -> Path:
    return Path("crypto/tests/data/mock_quotes.json")


class _MockQuoteImporter(QuoteImporter):
    def _download_quotes(self, symbol, time_unit):
        pass


@pytest.fixture(scope="module")
def quote_importer(quote_repository: QuotesPairRepository) -> QuoteImporter:
    return build(_MockQuoteImporter, quotes_repository=quote_repository)


@pytest.fixture(scope="module")
def mock_quote_json_folder() -> Path:
    return Path("crypto/tests/data/quotes/json/")


@pytest.fixture(scope="module")
def mock_quote_csv_folder() -> Path:
    return Path("crypto/tests/data/quotes/csv/")


@pytest.fixture(scope="module")
def quote_repo_config(
    mock_quote_csv_folder: Path, mock_quote_json_folder: Path
) -> QuotesPairRepository.Configuration:
    return QuotesPairRepository.Configuration(
        json_folder=mock_quote_json_folder, csv_folder=mock_quote_csv_folder
    )


@pytest.fixture(scope="module")
def quote_repository(
    quote_repo_config: QuotesPairRepository.Configuration,
) -> QuotesPairRepository:
    return build(QuotesPairRepository, config=quote_repo_config)
