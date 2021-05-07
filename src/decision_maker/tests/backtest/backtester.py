from crypto.models import Symbol
from decision_maker.backtest.backtest import Backtester
from decision_maker.models.strategy import Strategy


def test_backtester(backtester: Backtester, strategy: Strategy, symbol: Symbol):
    backtester.apply_strategy_to_symbol(strategy, symbol)
