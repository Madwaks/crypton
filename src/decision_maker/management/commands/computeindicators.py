import os
import sys

from django.core.management.base import BaseCommand

from utils.service_provider import provide


class Command(BaseCommand):
    help = "Loads initial companies into DB"

    def handle(self, *args, **options):
        sys.path.insert(0, os.getcwd())
        from decision_maker.utils.indicators.compute_indicators import IndicatorComputer

        computer = provide(IndicatorComputer)
        computer.compute_indicators_for_all()
