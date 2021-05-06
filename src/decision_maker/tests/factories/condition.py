import factory
from factory import SubFactory
from factory.fuzzy import FuzzyChoice

from decision_maker.models import Indicator


class ConditionFactory(factory.django.DjangoModelFactory):
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
    # base_name = CharField(max_length=128, choices=AvailableIndicators.choices)
    # operator = CharField(max_length=8, choices=Operator.choices)
    # name_to_compare = CharField(max_length=128, choices=AvailableIndicators.choices)
    # day_number = IntegerField(default=1)
    # condition = CharField(max_length=16, choices=LogicOp.choices)

    quote = SubFactory("core.tests.factories.quotes.QuotesFactory")
