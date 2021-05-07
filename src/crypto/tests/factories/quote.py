import factory
from factory import enums, Faker
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice

from crypto.models import Quote, Symbol
from crypto.tests.factories.symbol import SymbolFactory
from utils.enums import TimeUnits


class QuotesFactory(DjangoModelFactory):
    class Meta:
        model = Quote
        strategy = enums.BUILD_STRATEGY
        django_get_or_create = ("timestamp",)

    timestamp = Faker("unix_time")
    open = Faker("random_int", min=10, max=15)
    high = Faker("random_int", min=10, max=15)
    close = Faker("random_int", min=10, max=15)
    close_time = Faker("unix_time")
    low = Faker("random_int", min=5, max=10)
    volume = Faker("random_int", min=100, max=5000)
    time_unit = FuzzyChoice(TimeUnits.values)

    symbol: Symbol = None

    @factory.post_generation
    def symbol(self, create, extracted, **_kwargs):
        if extracted:
            self.symbol = extracted
        else:
            fake = factory.faker.faker.Faker()
            if fake.boolean() and Symbol.objects.exists():
                self.feature = Symbol.objects.get(
                    name=Symbol.objects.values_list("name", flat=True)[
                        fake.random_int(min=0, max=Symbol.objects.count() - 1)
                    ]
                )
            else:
                self.symbol = (
                    SymbolFactory.create() if create else SymbolFactory.build()
                )
