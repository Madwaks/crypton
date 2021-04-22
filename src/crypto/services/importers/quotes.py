import json
from pathlib import Path
from typing import Union

import docker
from injector import singleton, inject

from crypto.models import Symbol, Quote
from crypto.services.factories.quote import QuoteSymbolFactory
from crypto.services.repositories.pair import SymbolRepository
from crypto.services.repositories.quote import QuotesPairRepository
from utils.binance_client import BinanceClient
from utils.enums import TimeUnits


@singleton
class QuotesPairImporter:
    @inject
    def __init__(
        self,
        quote_factory: QuoteSymbolFactory,
        client: BinanceClient,
        quotes_repository: QuotesPairRepository,
        pair_repository: SymbolRepository
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
        json_file = self._quotes_repo.get_json_name_for_symbol(symbol, time_unit)
        quotes_json = json.loads(json_file.read_text())
        quotes = self._quote_factory.build_quote_from_pair(symbol, time_unit, quotes_json)
        Quote.objects.bulk_create(quotes)

    def _download_quotes(self, symbol, time_unit):
        client = docker.from_env()
        host_directory = Path("data/").absolute()
        client.containers.run(image="madwaks/crypto-downloader:1.2", command=f"importquotes --time-unit={time_unit} --pair={symbol}",
                              volumes={host_directory: {'bind': '/data', 'mode': 'rw'}})
