from django.db import models

from decision_maker.models.enums import (
    Operator,
    Condition as Conditions,
    AvailableIndicators,
)


class Condition(models.Model):
    name = models.CharField(max_length=128, choices=AvailableIndicators.choices)
    operator = models.CharField(max_length=8, choices=Operator.choices)
    other_name = models.CharField(max_length=128, choices=AvailableIndicators.choices)
    screener = models.ForeignKey(
        "decision_maker.Screener", related_name="conditions", on_delete=models.CASCADE
    )
    day_number = models.IntegerField(default=1)
    condition = models.CharField(max_length=16, choices=Conditions.choices)


class Screener(models.Model):
    name = models.CharField(max_length=64)
