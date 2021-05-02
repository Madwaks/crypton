from django.db import models
from django.db.models import CharField

from utils.enums import TimeUnits


class SymbolIndicator(models.Model):
    name = models.CharField(max_length=128, null=True)

    value = models.FloatField(null=True)

    symbol = models.ForeignKey(
        "crypto.Symbol", related_name="indicators", on_delete=models.SET_NULL, null=True
    )

    time_unit = CharField(
        choices=TimeUnits.choices, max_length=128, blank=True, null=True
    )

    def __str__(self) -> str:
        return f"{str(self.symbol)} {str(self.name)}"

    def __gt__(self, other: "SymbolIndicator") -> bool:
        return self.value > other.value

    def __lt__(self, other: "SymbolIndicator") -> bool:
        return self.value < other.value

    def __eq__(self, other: "SymbolIndicator") -> bool:
        return self.value == other.value

    def __hash__(self):
        return hash(str(self.pk) + str(self.name))

    class Meta:
        ordering = ("name",)
        constraints = (
            models.UniqueConstraint(
                fields=("name", "symbol"), name="unique_per_name_and_symbol"
            ),
        )

    def save(self, **kwargs):
        symbol = self.symbol
        if symbol and symbol.pk is None:
            symbol.save()
        self.symbol = symbol

        super().save(**kwargs)
