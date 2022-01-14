from datetime import datetime
from functools import cached_property

from django.db.models import (
    Model,
    FloatField,
    ForeignKey,
    SET_NULL,
    CharField,
    UniqueConstraint,
    Index,
)

from crypto.managers.quotes import QuoteManager
from decision_maker.services.repositories.indicator import find_nearest_supp_and_res
from utils.enums import TimeUnits


class Quote(Model):
    timestamp = CharField(max_length=512, default="")
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
        dt = datetime.fromtimestamp(int(self.timestamp) / 1000)
        return datetime(
            year=dt.year,
            month=dt.month,
            day=dt.day,
            hour=dt.hour,
            minute=dt.minute,
            second=dt.second,
        )

    @property
    def close_date(self):
        dt = datetime.fromtimestamp(int(self.close_time) / 1000)
        return datetime(
            year=dt.year,
            month=dt.month,
            day=dt.day,
            hour=dt.hour,
            minute=dt.minute,
            second=dt.second,
        )

    @cached_property
    def nearest_key_level(self):
        near_res, near_supp = find_nearest_supp_and_res(self)
        return near_res, near_supp

    class Meta:
        ordering = ("timestamp",)
        constraints = (
            UniqueConstraint(
                fields=("timestamp", "time_unit", "symbol"),
                name="unique_per_timestamp_tu_symbol",
            ),
        )
        indexes = [
            Index(fields=["timestamp", "symbol"]),
            Index(fields=["timestamp"], name="timestamp_idx"),
        ]
