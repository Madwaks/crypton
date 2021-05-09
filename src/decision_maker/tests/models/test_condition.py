import pytest
from pytest_factoryboy import register

from crypto.models import Quote
from crypto.tests.factories.quote import QuotesFactory
from decision_maker.models import Indicator
from decision_maker.models.conditions import Condition
from decision_maker.tests.factories.condition import ConditionFactory
from decision_maker.tests.factories.indicator import IndicatorFactory

register(ConditionFactory, "first_condition")
register(ConditionFactory, "second_condition")
register(ConditionFactory, "third_condition")
register(ConditionFactory, "fourth_condition")
register(ConditionFactory, "fifth_condition")
register(QuotesFactory)
register(IndicatorFactory, "indicator")
register(IndicatorFactory, "second_indicator")


@pytest.fixture(scope="function")
def quote_with_indicators(
    quote: Quote, indicator: Indicator, second_indicator: Indicator
):
    indicator.quote = quote
    second_indicator.quote = quote
    indicator.save()
    second_indicator.save()

    return quote


@pytest.mark.django_db
@pytest.mark.parametrize(
    "first_condition__base_name, first_condition__name_to_compare, first_condition__operator, first_condition__time_unit_before",
    [("MM7", "MM20", "<", 0)],
)
def test_condition(first_condition: Condition, quote_with_indicators: Quote):
    assert first_condition.is_fulfilled(quote_with_indicators)
