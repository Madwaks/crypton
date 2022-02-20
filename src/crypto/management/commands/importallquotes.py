import os
import sys

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
            tus = [TimeUnits.from_code("1m"), TimeUnits.from_code("5m")]
        quotes_storer = provide(QuoteImporter)

        from crypto.utils.etc import SYMBOLS_TO_COMPUTE

        for symbol in tqdm(SYMBOLS_TO_COMPUTE):
            for tu in tus:
                print(f"{symbol.name} // {tu.value}")
                quotes_storer.import_quotes(symbol=symbol, time_unit=tu)
