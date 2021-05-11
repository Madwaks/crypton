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
register(IndicatorFactory, "indicator", name="MM7", value=3)
register(IndicatorFactory, "indicator2", name="MM20", value=5)
register(IndicatorFactory, "indicator3", name="MM200", value=6)
register(IndicatorFactory, "indicator4", name="MM100", value=2)
register(IndicatorFactory, "indicator5", name="MM50", value=4)


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
    "first_condition__operator",
    [("MM7", "MM20", "<"), ("MM200", "MM20", ">"), ("MM20", "MM200", "<")],
)
def test_right_condition(first_condition: Condition, quote_with_indicators: Quote):
    assert first_condition.is_fulfilled(quote_with_indicators)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "first_condition__base_name, "
    "first_condition__name_to_compare, "
    "first_condition__operator",
    [("MM7", "MM20", ">"), ("MM50", "MM200", ">")],
)
def test_wrong_condition(first_condition: Condition, quote_with_indicators: Quote):
    assert not first_condition.is_fulfilled(quote_with_indicators)
