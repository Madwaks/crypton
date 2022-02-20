import json
from logging import getLogger
from pathlib import Path

from injector import singleton, inject
from pandas import DataFrame

from crypto.models import Symbol
from crypto.services.factories.symbol import SymbolFactory
from crypton import settings
from utils.binance_client import CryptoComClient, BinanceClient
from utils.kraken import KrakenClient

logger = getLogger("django")


@singleton
class SymbolImporter:
    @inject
    def __init__(
        self,
        symbol_factory: SymbolFactory,
        binance_client: BinanceClient,
        crypto_com_client: CryptoComClient,
        kraken_client: KrakenClient,
    ):
        self._symbol_factory = symbol_factory
        self._crypto_com_client = crypto_com_client
        self._kraken_client = kraken_client
        self._binance_client = binance_client

    @property
    def json_file_path(self) -> Path:
        return settings.CRYPTO_FOLDER_PATH / "available_pairs.json"

    def import_all_symbols(self):
        binance_symbols = self._binance_client.get_available_symbols()
        # symbols = self._kraken_client.get_tradable_pairs()
        # available_symbols = self._crypto_com_client.get_available_instruments()
        df = DataFrame(binance_symbols)  # + available_symbols + symbols)
        df["instrument_name"] = df["instrument_name"].map(
            lambda name: name.replace("_", "")
        )
        df = df.drop_duplicates(
            subset=["instrument_name", "quote_currency", "base_currency"]
        )
        self._import_symbols(
            json.loads(
                df[["instrument_name", "quote_currency", "base_currency"]].to_json(
                    orient="records"
                )
            )
        )

    def _import_symbols(self, symbols_json: list[dict]):
        symbols = self._symbol_factory.build_symbols(symbols_json)
        Symbol.objects.bulk_create(symbols)
        logger.info(f"[Symbols] Stored {len(symbols)} symbols")
