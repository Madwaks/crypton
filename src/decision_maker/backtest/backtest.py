from datetime import datetime
from logging import getLogger
from typing import TypeVar

from injector import singleton, inject

from crypto.models import Symbol, Quote, Portfolio
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

    def apply_to_symbol(self, symbol: Symbol, time_unit: TimeUnits):
        quotes: list[Quote] = symbol.quotes.filter(time_unit=time_unit.value).order_by(
            "timestamp"
        )
        portfolio = Portfolio(solde=2000)
        for current_quote in quotes:
            if current_quote.open_date < datetime(year=2019, month=1, day=1):
                continue

            signal = self._strat_factory._get_decision_for_quote(current_quote)
            next_quote = Quote.objects.get_next_quote(current_quote)
            if next_quote is None:
                continue
            if signal == Side.BUY:
                self._logger.info(f"Order BUY sent: {next_quote.open_date}")
                order = MarketOrder(
                    timestamp=next_quote.timestamp,
                    quantity=500,
                    symbol=symbol,
                    side=Side.BUY,
                )
                self._send_market_order(order, portfolio)
                self._send_stop_loss_order(order)
                assert portfolio.available_titres_for_symbol(symbol) >= 500
            elif (
                signal == Side.SELL
                and portfolio.available_titres_for_symbol(symbol) >= 500
            ):
                self._logger.info(f"Order SELL sent: {next_quote.open_date}")
                order = MarketOrder(
                    timestamp=next_quote.timestamp,
                    quantity=500,
                    symbol=symbol,
                    side=Side.SELL,
                )
                self._send_order(order, portfolio)

        breakpoint()
        portfolio.delete()

    def _send_market_order(self, order: "OrderType", portfolio: Portfolio):
        if order.side == Side.BUY:
            portfolio.open_position(order)
        elif order.side == Side.SELL:
            portfolio.close_position(order)
