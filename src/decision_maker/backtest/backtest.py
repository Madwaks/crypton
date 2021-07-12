from logging import getLogger
from typing import TypeVar
import more_itertools
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
        windowed_queryset = list(more_itertools.windowed(quotes, n=3))
        portfolio = Portfolio(solde=2000)
        current_order = None
        for previous_quote, current_quote, next_quote in windowed_queryset[10:]:
            signal = self._strat_factory._get_decision_for_quote(
                previous_quote, current_quote
            )
            if next_quote is None:
                continue
            if signal == Side.BUY and current_order is None:
                self._logger.info(f"Order BUY sent: {next_quote.open_date}")
                order = MarketOrder(
                    timestamp=next_quote.timestamp, symbol=symbol, side=Side.BUY
                )
                quantity = portfolio.get_nb_titres_to_buy(order.get_price())
                order.quantity = quantity

                self._send_market_order(order, portfolio)
                current_order = order
            elif signal == Side.SELL and current_order is not None:
                self._logger.info(f"Order SELL sent: {next_quote.open_date}")
                order = MarketOrder(
                    timestamp=next_quote.timestamp,
                    quantity=portfolio.available_titres_for_symbol(symbol),
                    symbol=symbol,
                    side=Side.SELL,
                )
                self._send_market_order(order, portfolio)
                current_order = None

        breakpoint()
        portfolio.delete()

    def _send_market_order(self, order: "OrderType", portfolio: Portfolio):
        if order.side == Side.BUY:
            portfolio.open_position(order)
        elif order.side == Side.SELL:
            portfolio.close_position(order)
