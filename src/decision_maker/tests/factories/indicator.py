import factory
from factory import SubFactory
from factory.fuzzy import FuzzyChoice

from decision_maker.models import Indicator


class IndicatorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Indicator
        strategy = factory.enums.BUILD_STRATEGY

    name = FuzzyChoice(Indicator.AvailableIndicators, getter=lambda c: c)
    value = factory.Faker(
        "pyfloat",
        left_digits=2,
        positive=True,
        max_value=50,
        min_value=2,
        right_digits=2,
    )

    quote = SubFactory("core.tests.factories.quotes.QuotesFactory")
