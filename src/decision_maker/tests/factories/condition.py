import factory
from factory.fuzzy import FuzzyChoice

from decision_maker.models.conditions import Condition
from decision_maker.models.enums import AvailableIndicators, Operator, LogicOp


class ConditionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Condition
        strategy = factory.enums.BUILD_STRATEGY

    base_name = FuzzyChoice(AvailableIndicators, getter=lambda c: c)
    operator = FuzzyChoice(Operator.choices)
    name_to_compare = FuzzyChoice(AvailableIndicators, getter=lambda c: c)
    day_number = factory.Faker("random_int", min_value=0, max_value=20)
    condition = FuzzyChoice(max_length=16, choices=LogicOp.choices)
