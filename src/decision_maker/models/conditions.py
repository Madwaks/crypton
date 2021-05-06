from django.db.models import Model, CharField, IntegerField

from decision_maker.models.enums import Operator, AvailableIndicators, LogicOp


class Condition(Model):
    base_name = CharField(max_length=128, choices=AvailableIndicators.choices)
    operator = CharField(max_length=8, choices=Operator.choices)
    name_to_compare = CharField(max_length=128, choices=AvailableIndicators.choices)
    day_number = IntegerField(default=1)
    condition = CharField(max_length=16, choices=LogicOp.choices)

    def __str__(self):
        return f"{self.base_name} {self.operator} {self.name_to_compare}"
