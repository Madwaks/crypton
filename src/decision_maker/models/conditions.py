from typing import TYPE_CHECKING

from django.db.models import Model, CharField, UniqueConstraint

if TYPE_CHECKING:
    from crypto.models import Quote
from decision_maker.models.enums import Operator, AvailableIndicators, LogicOp


class Condition(Model):
    base_name = CharField(max_length=128, choices=AvailableIndicators.choices)
    operator = CharField(max_length=8, choices=Operator.choices)
    name_to_compare = CharField(max_length=128, choices=AvailableIndicators.choices)
    condition = CharField(max_length=16, choices=LogicOp.choices)

    def __str__(self):
        return f"{self.base_name} {self.operator} {self.name_to_compare}"

    def is_fulfilled(self, quote: "Quote") -> bool:
        base_indicator = quote.indicators.get(name=self.base_name)
        compared_indicator = quote.indicators.get(name=self.name_to_compare)

        return eval(
            f"{base_indicator.value} {self.operator} {compared_indicator.value}"
        )

    class Meta:
        ordering = ("base_name", "name_to_compare")
        constraints = (
            UniqueConstraint(
                fields=("base_name", "name_to_compare", "operator"),
                name="unique_per_indicators_and_operator",
            ),
        )

    def save(self, **kwargs):
        if self.pk:
            return
        else:
            super().save(**kwargs)
