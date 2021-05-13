import factory

from decision_maker.models import Strategy, Condition


class StrategyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Strategy
        strategy = factory.enums.BUILD_STRATEGY

    conditions: set[Condition] = None

    @factory.post_generation
    def conditions(self, create, extracted, **_kwargs):
        if not create:
            return
        if extracted:
            for condition in extracted:
                self.conditions.add(condition)
