from datetime import datetime

from django.db.models import (
    Model,
    FloatField,
    ForeignKey,
    SET_NULL,
    CharField,
    UniqueConstraint,
)

from crypto.managers.quotes import QuoteManager
from utils.enums import TimeUnits


class Quote(Model):
    timestamp = CharField(max_length=512, primary_key=True)
    open = FloatField(max_length=128, verbose_name="open_price")
    close = FloatField(max_length=128, verbose_name="close_price")
    high = FloatField(max_length=128, verbose_name="high_price")
    low = FloatField(max_length=128, verbose_name="low_price")
    volume = FloatField(verbose_name="volumes")
    symbol = ForeignKey(
        "crypto.Symbol",
        related_name="quotes",
        max_length=128,
        null=True,
        on_delete=SET_NULL,
    )
    close_time = CharField(max_length=512, null=True, blank=True)
    time_unit = CharField(
        choices=TimeUnits.choices, max_length=128, blank=True, null=True
    )
    objects = QuoteManager()

    def __str__(self):
        return f"{self.symbol.name} - {self.open_date} - {self.time_unit}"

    @property
    def open_date(self):
        return datetime.fromtimestamp(int(self.timestamp) / 1000)

    @property
    def close_date(self):
        return datetime.fromtimestamp(int(self.close_time) / 1000)

    class Meta:
        ordering = ("timestamp",)
        constraints = (
            UniqueConstraint(fields=("timestamp",), name="unique_per_timestamp"),
        )
