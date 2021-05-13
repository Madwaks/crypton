import pytest
from pytest_factoryboy import register

from crypto.models import Quote
from crypto.tests.factories.quote import QuotesFactory
from decision_maker.models import Strategy, Indicator
from decision_maker.models.conditions import Condition
from decision_maker.tests.factories.condition import ConditionFactory
from decision_maker.tests.factories.indicator import IndicatorFactory
from decision_maker.tests.factories.strategy import StrategyFactory

register(QuotesFactory)
register(IndicatorFactory, "indicator", name="MM7", value=3)
register(IndicatorFactory, "indicator2", name="MM20", value=5)
register(IndicatorFactory, "indicator3", name="MM200", value=6)
register(IndicatorFactory, "indicator4", name="MM100", value=2)
register(IndicatorFactory, "indicator5", name="MM50", value=4)

register(ConditionFactory, "first_condition")
register(ConditionFactory, "second_condition")
register(ConditionFactory, "third_condition")
register(ConditionFactory, "fourth_condition")

register(StrategyFactory)


@pytest.fixture(scope="function")
def quote_with_indicators(
    quote: Quote,
    indicator: Indicator,
    indicator2: Indicator,
    indicator3: Indicator,
    indicator4: Indicator,
    indicator5: Indicator,
):
    indicator.quote = quote
    indicator2.quote = quote
    indicator3.quote = quote
    indicator4.quote = quote
    indicator5.quote = quote
    indicator.save()
    indicator2.save()
    indicator3.save()
    indicator4.save()
    indicator5.save()

    yield quote
    indicator.delete()
    indicator2.delete()
    indicator3.delete()
    indicator4.delete()
    indicator5.delete()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "first_condition__base_name, "
    "first_condition__name_to_compare, "
    "first_condition__operator, "
    "first_condition__condition",
    [("MM7", "MM20", "<", "AND"), ("MM7", "MM20", ">", "OR")],
)
@pytest.mark.parametrize(
    "second_condition__base_name, "
    "second_condition__name_to_compare, "
    "second_condition__operator, "
    "second_condition__condition",
    [("MM7", "MM200", "<=", "AND"), ("MM50", "MM100", "<=", "OR")],
)
@pytest.mark.parametrize(
    "third_condition__base_name, "
    "third_condition__name_to_compare, "
    "third_condition__operator, "
    "third_condition__condition",
    [("MM20", "MM100", ">=", "AND"), ("MM7", "MM100", "<=", "OR")],
)
@pytest.mark.parametrize(
    "fourth_condition__base_name, "
    "fourth_condition__name_to_compare, "
    "fourth_condition__operator, "
    "fourth_condition__condition",
    [("MM20", "MM100", ">=", "AND")],
)
def test_multiple_conditions(
    strategy: Strategy,
    first_condition: Condition,
    second_condition: Condition,
    third_condition: Condition,
    fourth_condition: Condition,
    quote_with_indicators: Quote,
):
    first_condition.save()
    second_condition.save()
    third_condition.save()
    fourth_condition.save()
    strategy.conditions.set(
        [first_condition, second_condition, third_condition, fourth_condition]
    )

    assert strategy.fulfill_conditions(quote_with_indicators)

    strategy.delete()
    first_condition.delete()
    second_condition.delete()
    third_condition.delete()
    fourth_condition.delete()
