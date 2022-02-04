from functools import cached_property
from typing import TYPE_CHECKING

from django.db.models import (
    Model,
    FloatField,
    SET_NULL,
    UniqueConstraint,
    OneToOneField,
    Index,
)

if TYPE_CHECKING:
    from crypto.models import Quote


class Distance(Model):
    MM7 = FloatField(max_length=128, verbose_name="mm7", null=True)
    MM20 = FloatField(max_length=128, verbose_name="mm20", null=True)
    MM50 = FloatField(max_length=128, verbose_name="mm50", null=True)
    MM100 = FloatField(max_length=128, verbose_name="mm100", null=True)
    MM200 = FloatField(max_length=128, verbose_name="mm200", null=True)
    support = FloatField(max_length=128, verbose_name="support")
    resistance = FloatField(max_length=128, verbose_name="resistance")
    quote: "Quote" = OneToOneField(
        "crypto.Quote",
        related_name="distances",
        max_length=128,
        null=True,
        on_delete=SET_NULL,
    )

    def __str__(self):
        return f"Distance {self.quote}"

    @cached_property
    def abs_mm7(self) -> float:
        return abs(self.MM7)

    @cached_property
    def abs_mm_20(self) -> float:
        return abs(self.MM20)

    @cached_property
    def abs_mm_50(self) -> float:
        return abs(self.MM50)

    @cached_property
    def abs_mm_100(self) -> float:
        return abs(self.MM100)

    @cached_property
    def abs_mm_200(self) -> float:
        return abs(self.MM200)

    class Meta:
        constraints = (UniqueConstraint(fields=("quote",), name="unique_per_quote"),)
        indexes = [Index(fields=["quote"])]
