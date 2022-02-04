from logging import getLogger
from pathlib import Path

from injector import singleton, inject

from crypto.models import Symbol
from crypto.services.factories.symbol import SymbolFactory
from crypton import settings
from utils.binance_client import CryptoComClient

logger = getLogger("django")


@singleton
class SymbolImporter:
    @inject
    def __init__(
        self, symbol_factory: SymbolFactory, crypto_com_client: CryptoComClient
    ):
        self._symbol_factory = symbol_factory
        self._crypto_com_client = crypto_com_client

    @property
    def json_file_path(self) -> Path:
        return settings.CRYPTO_FOLDER_PATH / "available_pairs.json"

    def import_all_symbols(self):
        available_symbols = self._crypto_com_client.get_available_instruments()
        self._import_symbols(available_symbols)

    def _import_symbols(self, symbols_json: list[dict]):
        symbols = self._symbol_factory.build_symbols(symbols_json)
        Symbol.objects.bulk_create(symbols)
        logger.info(f"[Symbols] Stored {len(symbols)} symbols")
