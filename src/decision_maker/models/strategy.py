from django.db.models import Model, ManyToManyField

from decision_maker.models.enums import LogicOp


class Strategy(Model):
    conditions = ManyToManyField(
        "decision_maker.Condition", related_name="strategies", max_length=128
    )

    def fulfill_conditions(self) -> bool:
        and_condition = [
            cond.is_fulfilled
            for cond in self.conditions
            if cond.condition == LogicOp.AND
        ]
        or_condition = [
            cond.is_fulfilled
            for cond in self.conditions
            if cond.condition == LogicOp.OR
        ]

        return all(and_condition) and any(or_condition)
