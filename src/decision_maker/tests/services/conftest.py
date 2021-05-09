import pytest

from decision_maker.services.factories.indicators import DataFrameIndicatorFactory
from utils.service_provider import provide


@pytest.fixture(scope="module")
def df_indicator_factory() -> DataFrameIndicatorFactory:
    return provide(DataFrameIndicatorFactory)
