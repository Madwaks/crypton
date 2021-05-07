from factory import enums
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice

from crypto.models import Symbol
from crypto.tests.data.list_name import (
    quote_asset_mock,
    mock_base_assets,
    list_mock_symbols,
)


class SymbolFactory(DjangoModelFactory):
    class Meta:
        model = Symbol
        strategy = enums.BUILD_STRATEGY
        django_get_or_create = ("name", "base_asset", "quote_asset")

    name: str = FuzzyChoice(list_mock_symbols)

    base_asset = FuzzyChoice(mock_base_assets)
    quote_asset = FuzzyChoice(quote_asset_mock)
    order_types = []
