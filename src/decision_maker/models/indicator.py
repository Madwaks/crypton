from django.db import models

from decision_maker.managers.indicator import IndicatorManager
from decision_maker.models.enums import AvailableIndicators


class Indicator(models.Model):
    objects = IndicatorManager()

    name = models.CharField(
        max_length=128, choices=AvailableIndicators.choices, null=True
    )

    value = models.FloatField(null=True)

    quote = models.ForeignKey(
        "crypto.Quote", related_name="indicators", on_delete=models.SET_NULL, null=True
    )

    def __str__(self) -> str:
        return f"{str(self.quote)} {str(self.name)}"

    def __add__(self, other):
        return self.value + other.value

    def __sub__(self, other):
        return self.value - other.value

    def __gt__(self, other):
        return self.value > other.value

    def __lt__(self, other):
        return self.value < other.value

    def __eq__(self, other):
        return self.value == other.value

    def __hash__(self):
        return hash(str(self.pk) + str(self.name))

    class Meta:
        ordering = ("name",)
        constraints = (
            models.UniqueConstraint(
                fields=("name", "quote"), name="unique_per_name_and_quote"
            ),
        )

    def save(self, **kwargs):
        quote = self.quote
        if quote and quote.pk is None:
            quote.save()
        self.quote = quote

        super().save(**kwargs)
