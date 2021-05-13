from injector import singleton, inject

from crypto.models import Symbol
from utils.enums import TimeUnits


@singleton
class Backtester:
    @inject
    def __init__(self):
        pass

    def apply_to_symbol(self, symbol: Symbol, time_unit: TimeUnits):
        quotes = symbol.quotes.filter(time_unit=time_unit.value).order_by("timestamp")

        for current_quote in quotes:
            pass
