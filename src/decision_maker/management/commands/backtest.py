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
            "--time-unit", choices=self.choices, type=str, required=False, default="4h"
        )
        parser.add_argument("--symbol", type=str, required=False, default="ETHBTC")

    def handle(self, *args, **options):
        sys.path.insert(0, os.getcwd())

        from utils.service_provider import provide
        from utils.enums import TimeUnits

        tu = TimeUnits.from_code(options["time_unit"])

        from decision_maker.backtest.backtest import Backtester
        from crypto.models import Symbol

        backtester = provide(Backtester)
        backtester.apply_to_symbol(
            symbol=Symbol.objects.get(name="ETHBTC"), time_unit=tu
        )
