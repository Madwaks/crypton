from logging import getLogger
from typing import TypeVar

import more_itertools
from injector import singleton, inject

from crypto.models import Symbol, Quote, Portfolio, Position
from crypto.models.order import MarketOrder, Order
from crypto.utils.enums import Side
from decision_maker.services.factories.strategy import StrategyFactory
from utils.binance_client import TestClient
from utils.enums import TimeUnits

OrderType = TypeVar("OrderType", bound=Order)


@singleton
class Backtester:
    @inject
    def __init__(self, test_client: TestClient, strategy_factory: StrategyFactory):
        self._logger = getLogger("django")
        self._test_client = test_client
        self._strat_factory = strategy_factory
        self._portfolio = Portfolio(solde=2000)
        self._stop_loss_percent = 0.05

    def apply_to_symbol(self, symbol: Symbol, time_unit: TimeUnits):
        quotes: list[Quote] = symbol.quotes.filter(time_unit=time_unit.value).order_by(
            "timestamp"
        )
        windowed_queryset = list(more_itertools.windowed(quotes, n=3))
        current_position = None
        for previous_quote, current_quote, next_quote in windowed_queryset[10:]:
            signal = self._strat_factory._get_decision_for_quote(
                previous_quote, current_quote
            )
            if next_quote is None:
                continue
            if signal == Side.BUY and current_position is None:
                current_position = self._send_buy_order(next_quote)
            elif current_position is not None and (
                signal == Side.SELL
                or min(
                    [
                        current_quote.open,
                        current_quote.low,
                        current_quote.high,
                        current_quote.close,
                    ]
                )
                < (
                    current_position.pru
                    - current_position.pru * self._stop_loss_percent
                )
            ):
                self._send_sell_order(next_quote)
                current_position = None
        print(self._portfolio.solde)

    def _send_buy_order(self, quote: Quote) -> "Position":
        self._logger.info(f"Order BUY sent: {quote.open_date}")
        order = MarketOrder(
            timestamp=quote.timestamp, symbol=quote.symbol, side=Side.BUY
        )
        quantity = self._portfolio.get_nb_titres_to_buy(order.get_price())
        order.quantity = quantity

        return self._send_market_order(order, self._portfolio)

    def _send_sell_order(self, quote: Quote) -> "Position":
        self._logger.info(f"Order SELL sent: {quote.open_date}")
        order = MarketOrder(
            timestamp=quote.timestamp,
            quantity=self._portfolio.available_titres_for_symbol(quote.symbol),
            symbol=quote.symbol,
            side=Side.SELL,
        )
        return self._send_market_order(order, self._portfolio)

    def _send_market_order(self, order: "OrderType", portfolio: Portfolio) -> Position:
        if order.side == Side.BUY:
            return portfolio.open_position(order)
        elif order.side == Side.SELL:
            return portfolio.close_position(order)
