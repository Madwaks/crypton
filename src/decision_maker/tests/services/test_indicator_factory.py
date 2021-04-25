# import pytest

# from core.models import Company
# from decision_maker.services.factories.indicators import DataFrameIndicatorFactory


# @pytest.mark.django_db
# def test_indicator_factory(
#     company: Company, df_indicator_factory: DataFrameIndicatorFactory
# ):
#     quotes_as_df = company.quotes.get_as_dataframe()


#    df = df_indicator_factory.build_indicators_from_dataframe(quotes_as_df)
