import os
import sys

from django.core.management import BaseCommand
from tqdm import tqdm

from crypto.models import Symbol
from crypto.services.importers.quotes import QuotesPairImporter
from utils.enums import TimeUnits


class Command(BaseCommand):
    help = "Loads initial companies into DB"

    @property
    def choices(self) -> list[str]:
        return ["1m", "5m", "15m", "30m", "1h", "4h", "1d", "1w", "1M"]

    def add_arguments(self, parser):
        parser.add_argument(
            "--time-unit", choices=self.choices, type=str, required=True
        )

    def handle(self, *args, **options):
        sys.path.insert(0, os.getcwd())

        from utils.service_provider import provide

        tu = TimeUnits.from_code(options["time_unit"])
        quotes_storer = provide(QuotesPairImporter)

        from crypto.utils.etc import SYMBOLS_TO_COMPUTE

        for symbol in tqdm(SYMBOLS_TO_COMPUTE):
            quotes_storer.import_quotes(symbol=symbol, time_unit=tu)
