from typing import Set

from factory import enums, post_generation
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice

from crypto.models import Symbol, Quote
from crypto.tests.data.list_name import (
    quote_asset_mock,
    mock_base_assets,
    list_mock_symbols,
)
from crypto.tests.factories.quote import QuotesFactory


class SymbolFactory(DjangoModelFactory):
    class Meta:
        model = Symbol
        strategy = enums.CREATE_STRATEGY
        django_get_or_create = ("name", "base_asset", "quote_asset")

    name: str = FuzzyChoice(list_mock_symbols)

    base_asset = FuzzyChoice(mock_base_assets)
    quote_asset = FuzzyChoice(quote_asset_mock)
    order_types = []
    # quotes = RelatedFactoryList(
    # 	"crypto.tests.factories.quote.QuotesFactory",
    # 	factory_related_name="symbol",
    # 	size=201,
    # )
    quotes: Set[Quote] = None

    @post_generation
    def quotes(self, create, extracted, **_kwargs):
        if extracted:
            while len(self.quotes.all()) <= 205:
                self.quotes.add(
                    QuotesFactory.create(symbol=self)
                    if create
                    else QuotesFactory.build(symbol=self)
                )
        else:
            self.quotes.add(
                QuotesFactory.create(symbol=self)
                if create
                else QuotesFactory.build(symbol=self)
            )
