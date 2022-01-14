import os
import sys

from django.core.management import BaseCommand


class Command(BaseCommand):
    help = "Loads initial companies into DB"

    @property
    def choices(self) -> list[str]:
        return ["1m", "5m", "15m", "30m", "1h", "4h", "1d", "1w", "1M"]

    def add_arguments(self, parser):
        parser.add_argument(
            "--time-unit", choices=self.choices, type=str, required=True
        )
        parser.add_argument("--symbol", type=str, required=True)

    def handle(self, *args, **options):
        sys.path.insert(0, os.getcwd())

        from utils.service_provider import provide
        from utils.enums import TimeUnits
        from decision_maker.utils.indicators.compute_indicators import IndicatorComputer

        symbol: str = options["symbol"]
        tu = TimeUnits.from_code(options["time_unit"])

        computer = provide(IndicatorComputer)
        computer.compute_indicators_for_symbol(symbol=symbol, time_unit=tu)
