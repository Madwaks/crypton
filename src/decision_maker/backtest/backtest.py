from injector import singleton, inject

from crypto.models import Symbol
from decision_maker.models.strategy import Strategy


@singleton
class Backtester:
    @inject
    def __init__(self):
        pass

    def apply_strategy_to_symbol(
        self, strategy: Strategy, symbol: Symbol
    ):  # -> "Result":
        quotes = symbol.quotes.order_by("timestamp")

        for currenr_quote in quotes:
            if strategy.fulfill_conditions():
                self._send_order(currenr_quote)
            else:
                continue
