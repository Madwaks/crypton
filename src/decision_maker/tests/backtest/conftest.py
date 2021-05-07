import pytest

from decision_maker.backtest.backtest import Backtester
from utils.service_provider import provide


@pytest.fixture(scope="module")
def backtester() -> Backtester:
    return provide(Backtester)
