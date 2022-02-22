import os
import sys
from itertools import repeat
from multiprocessing import Pool

from django.core.management import BaseCommand
from tqdm import tqdm

from crypto.services.importers.quotes import QuoteImporter
from utils.enums import TimeUnits


class Command(BaseCommand):
    help = "Loads initial companies into DB"

    @property
    def choices(self) -> list[str]:
        return ["1m", "5m", "15m", "30m", "1h", "4h", "1d", "1w", "1M"]

    def add_arguments(self, parser):
        parser.add_argument("--time-unit", choices=self.choices, type=str)

    def handle(self, *args, **options):
        sys.path.insert(0, os.getcwd())

        from utils.service_provider import provide

        if options["time_unit"]:
            tus = [TimeUnits.from_code(options["time_unit"])]
        else:
            tus = [
                TimeUnits.from_code("15m"),
                TimeUnits.from_code("5m"),
                TimeUnits.from_code("4h"),
            ]
        quotes_storer = provide(QuoteImporter)

        from crypto.utils.etc import SYMBOLS_TO_COMPUTE

        self._update_all_symbols(SYMBOLS_TO_COMPUTE, tus, quotes_storer)

    def _update_all_symbols(
        self, symbols: list, time_units: list[TimeUnits], quotes_storer: QuoteImporter
    ):
        for symbol in tqdm(symbols):
            for tu in time_units:
                quotes_storer.import_quotes(symbol=symbol, time_unit=tu)
