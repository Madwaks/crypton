from factory import SubFactory, enums, Faker
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice

from crypto.models import Quote
from utils.enums import TimeUnits


class QuotesFactory(DjangoModelFactory):
    class Meta:
        model = Quote
        strategy = enums.BUILD_STRATEGY
        django_get_or_create = ("timestamp", "symbol")

    timestamp = Faker("unix_time")
    open = Faker("random_int", min=10, max=15)
    high = Faker("random_int", min=10, max=15)
    close = Faker("unix_time")
    low = Faker("random_int", min=5, max=10)
    volume = Faker("random_int", min=100, max=5000)
    time_unit = FuzzyChoice(TimeUnits.values)
    symbol = SubFactory("crypto.tests.factories.symbol.SymbolFactory")
