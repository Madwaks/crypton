import pytest
from pytest_factoryboy import register

from core.tests.factories.company import CompanyFactory
from core.tests.factories.company_info import CompanyInfoFactory
from core.tests.factories.quotes import QuotesFactory
from decision_maker.services.factories.indicators import DataFrameIndicatorFactory
from decision_maker.tests.factories.indicator import IndicatorFactory
from utils.service_provider import provide

register(CompanyInfoFactory)
register(CompanyFactory, quotes=202)
register(QuotesFactory)
register(IndicatorFactory)


@pytest.fixture(scope="module")
def df_indicator_factory() -> DataFrameIndicatorFactory:
    return provide(DataFrameIndicatorFactory)
