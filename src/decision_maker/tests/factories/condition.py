import factory
from factory.fuzzy import FuzzyChoice

from decision_maker.models.conditions import Condition
from decision_maker.models.enums import AvailableIndicators, Operator, LogicOp


class ConditionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Condition
        strategy = factory.enums.BUILD_STRATEGY

    base_name = FuzzyChoice(choices=AvailableIndicators.values)
    operator = FuzzyChoice(choices=Operator.values)
    name_to_compare = FuzzyChoice(choices=AvailableIndicators.values)
    time_unit_before = factory.Faker("random_int", min=0, max=20)
    condition = FuzzyChoice(choices=LogicOp.values)
