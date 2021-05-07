from injector import singleton, inject

from decision_maker.models.conditions import Condition
from decision_maker.models.strategy import Strategy


@singleton
class StrategyFactory:
    @inject
    def __init__(self):
        pass

    def build_strategy_from_conditions(self, conditions: list[Condition]) -> Strategy:
        return Strategy(conditions=conditions)
