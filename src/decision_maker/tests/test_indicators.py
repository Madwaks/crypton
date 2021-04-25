import pytest
from pytest_factoryboy import register

from core.tests.factories.company import CompanyFactory
from core.tests.factories.company_info import CompanyInfoFactory
from core.tests.factories.quotes import QuotesFactory
from decision_maker.models import Indicator
from decision_maker.tests.factories.indicator import IndicatorFactory

register(CompanyInfoFactory)
register(CompanyFactory)
register(QuotesFactory)
register(IndicatorFactory)
register(IndicatorFactory, "other_indicator")


@pytest.mark.django_db
def test_indicator(indicator: Indicator):
    assert indicator.name.value in Indicator.AvailableIndicators.values
    assert str(indicator) == f"{str(indicator.quote)} {str(indicator.name)}"
    assert hash(indicator) == hash(str(indicator.pk) + indicator.name)


@pytest.mark.django_db
@pytest.mark.parametrize("other_indicator__value", [3])
@pytest.mark.parametrize("indicator__value", [3])
def test_eq_indicator(indicator: Indicator, other_indicator: Indicator):
    assert indicator == other_indicator


@pytest.mark.django_db
@pytest.mark.parametrize("other_indicator__value", [3])
@pytest.mark.parametrize("indicator__value", [5])
def test_lt_indicator(indicator: Indicator, other_indicator: Indicator):
    assert other_indicator < indicator


@pytest.mark.django_db
@pytest.mark.parametrize("other_indicator__value", [5])
@pytest.mark.parametrize("indicator__value", [3])
def test_gt_indicator(indicator: Indicator, other_indicator: Indicator):
    assert other_indicator > indicator


@pytest.mark.django_db
def test_add_indicator(indicator: Indicator, other_indicator: Indicator):
    assert other_indicator + indicator == other_indicator.value + indicator.value
