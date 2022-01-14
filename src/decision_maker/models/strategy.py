from typing import TYPE_CHECKING

from django.db.models import Model, ManyToManyField

if TYPE_CHECKING:
    from crypto.models import Quote
from decision_maker.models.enums import LogicOp


class Strategy(Model):
    conditions = ManyToManyField(
        "decision_maker.Condition", related_name="strategies", max_length=128
    )

    def apply_to_quote(self, quote: "Quote"):

        pass

    def fulfill_conditions(self, quote: "Quote") -> bool:

        and_condition = [
            cond.is_fulfilled(quote)
            for cond in self.conditions.all()
            if cond.condition == LogicOp.AND
        ]
        or_condition = [
            cond.is_fulfilled(quote)
            for cond in self.conditions.all()
            if cond.condition == LogicOp.OR
        ]

        return (
            all(and_condition)
            if and_condition
            else True and any(or_condition)
            if or_condition
            else True
        )
