import json
from logging import getLogger
from pathlib import Path
from typing import Union

import docker
from django.db import IntegrityError
from injector import singleton, inject

from crypto.models import Symbol, Quote
from crypto.services.factories.quote import QuoteSymbolFactory
from crypto.services.repositories.pair import SymbolRepository
from crypto.services.repositories.quote import QuotesPairRepository
from utils.binance_client import BinanceClient
from utils.enums import TimeUnits

logger = getLogger("django")


@singleton
class QuotesPairImporter:
    @inject
    def __init__(
        self,
        quote_factory: QuoteSymbolFactory,
        client: BinanceClient,
        quotes_repository: QuotesPairRepository,
        pair_repository: SymbolRepository,
    ):
        self._quote_factory = quote_factory
        self._client = client
        self._quotes_repo = quotes_repository
        self._symbol_repo = pair_repository

    def import_all_quotes(self, time_unit: str):
        for pair in Symbol.objects.all():
            self.import_quotes(pair, TimeUnits.from_code(time_unit))

    def import_quotes(self, symbol: Union[str, Symbol], time_unit: TimeUnits):
        self._download_quotes(symbol, time_unit)
        symbol = self._symbol_repo.get_symbol_from_code(symbol)
        json_file = self._quotes_repo.get_json_path_for_symbol(symbol, time_unit)
        quotes_json = json.loads(json_file.read_text())
        quotes = self._quote_factory.build_quote_for_symbol(
            symbol, time_unit, quotes_json
        )
        self._save_objects(quotes)

    def _download_quotes(self, symbol, time_unit):
        client = docker.from_env()
        host_directory = Path("data/").absolute()
        client.containers.run(
            image="madwaks/crypto-downloader:1.2",
            command=f"importquotes --time-unit={time_unit} --symbol={symbol}",
            volumes={host_directory: {"bind": "/data", "mode": "rw"}},
            remove=True,
        )

    def _save_objects(self, quotes: list[Quote]):
        try:
            Quote.objects.bulk_create(quotes)
            logger.info(f"[Quotes] Stored {len(quotes)} quotes")
        except IntegrityError as err:
            logger.info(err)
            logger.info("[Quote] Trying to save objects 1by1 ")

            for quote in quotes:
                if not Quote.objects.filter(timestamp=quote.timestamp).exists():
                    quote.save()
