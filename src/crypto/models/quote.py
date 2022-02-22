from datetime import datetime
from functools import cached_property
from typing import TYPE_CHECKING

from dateutil import tz
from django.db.models import (
    Model,
    FloatField,
    ForeignKey,
    SET_NULL,
    CharField,
    UniqueConstraint,
    Index,
    IntegerField,
    BooleanField,
)

from crypto.managers.quotes import QuoteManager

if TYPE_CHECKING:
    from crypto.models import Symbol
from decision_maker.services.repositories.indicator import find_nearest_supp_and_res
from utils.enums import TimeUnits


class Quote(Model):
    timestamp = IntegerField(default=0)
    open = FloatField(max_length=128, verbose_name="open_price")
    close = FloatField(max_length=128, verbose_name="close_price")
    high = FloatField(max_length=128, verbose_name="high_price")
    low = FloatField(max_length=128, verbose_name="low_price")
    volume = FloatField(verbose_name="volumes")
    symbol: "Symbol" = ForeignKey(
        "crypto.Symbol",
        related_name="quotes",
        max_length=128,
        null=True,
        on_delete=SET_NULL,
    )
    close_time = IntegerField(default=0)
    time_unit = CharField(
        choices=TimeUnits.choices, max_length=128, blank=True, null=True
    )
    is_last = BooleanField(default=False)
    objects = QuoteManager()

    def __str__(self):
        return f"{self.symbol.name} - {self.close_date} - {self.time_unit}"

    @property
    def open_date(self):
        dt = datetime.fromtimestamp(self.timestamp, tz=tz.tzutc())
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
        dt = datetime.fromtimestamp(self.close_time, tz=tz.tzutc())
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
            Index(fields=["timestamp", "symbol", "time_unit"]),
            Index(fields=["time_unit"]),
            Index(fields=["symbol", "time_unit"]),
            Index(fields=["timestamp"]),
        ]
