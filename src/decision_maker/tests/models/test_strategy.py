import pytest
from pytest_factoryboy import register

from decision_maker.models import Strategy
from decision_maker.models.conditions import Condition
from decision_maker.tests.factories.condition import ConditionFactory

register(ConditionFactory, "first_condition")
register(ConditionFactory, "second_condition")
register(ConditionFactory, "third_condition")
register(ConditionFactory, "fourth_condition")
register(ConditionFactory, "fifth_condition")


@pytest.mark.django_db
@pytest.mark.parametrize(
    "first_condition__base_name, "
    "first_condition__name_to_compare, "
    "first_condition__operator, "
    "first_condition__condition",
    [("MM7", "MM20", ">", "AND")],
)
@pytest.mark.parametrize(
    "second_condition__base_name, "
    "second_condition__name_to_compare, "
    "second_condition__operator, "
    "second_condition__condition",
    [("MM7", "MM200", "<=", "AND")],
)
@pytest.mark.parametrize(
    "third_condition__base_name, "
    "third_condition__name_to_compare, "
    "third_condition__operator, "
    "third_condition__condition",
    [("MM20", "MM100", "<=", "AND")],
)
def test_multiple_conditions(
    first_condition: Condition, second_condition: Condition, third_condition: Condition
):
    strategy = Strategy()
    strategy.conditions.set([first_condition, second_condition, third_condition])
    breakpoint()
