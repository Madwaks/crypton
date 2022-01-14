import json
from datetime import timedelta
from logging import getLogger
from pathlib import Path
from typing import Union, Any

import docker
from django.db import IntegrityError
from injector import singleton, inject

from crypto.models import Symbol, Quote
from crypto.services.factories.quote import QuoteSymbolFactory
from crypto.services.repositories.pair import SymbolRepository
from crypto.services.repositories.quote import QuotesPairRepository
from crypto.utils.etc import open_date, close_date
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
        symbol = Symbol.objects.get(name=symbol)
        json_file = self._quotes_repo.get_json_path_for_symbol(symbol, time_unit)
        quotes_json = json.loads(json_file.read_text())
        timestamps = set(symbol.quotes.values_list("timestamp", flat=True))

        quotes = self._quote_factory.build_quote_for_symbol(
            symbol,
            time_unit,
            [
                quote
                for quote in quotes_json
                if quote.get("timestamp") not in timestamps
                and self._is_valid_quote(quote)
            ],
        )
        if quotes:
            self._save_objects(quotes)

    def _is_valid_quote(self, quote: dict[str, Any]):
        return close_date(quote) < open_date(quote) + timedelta(hours=3, minutes=30)

    def _download_quotes(self, symbol, time_unit):
        client = docker.from_env()
        host_directory = Path("data/").absolute()
        client.containers.run(
            image="madwaks/crypto-downloader:latest",
            command=f"importquotes --time-unit={time_unit} --symbol={symbol}",
            volumes={host_directory: {"bind": "/data", "mode": "rw"}},
            remove=True,
        )

    def _save_objects(self, quotes: list[Quote]):
        try:
            Quote.objects.bulk_create(quotes)
            logger.info(f"[Quotes] Stored {len(quotes)} quotes for {quotes[0].symbol}")
        except IntegrityError as err:
            logger.info(err)
            logger.info("[Quote] Trying to save objects 1by1 ")
            for quote in quotes:
                quote.save()
