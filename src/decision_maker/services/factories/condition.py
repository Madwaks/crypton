import re

from injector import singleton

from decision_maker.models import Condition


@singleton
class ConditionFactory:
    def build_condition_from_str(self, conditions_as_str: str) -> Condition:
        self._parse_condition_from_str(conditions_as_str)

    def _parse_condition_from_str(self, conditions_as_str: str) -> list[str]:
        re.split("and | or", conditions_as_str)
