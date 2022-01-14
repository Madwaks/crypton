from datetime import datetime

from django.db.models import (
    Model,
    FloatField,
    ForeignKey,
    SET_NULL,
    CharField,
    UniqueConstraint,
    OneToOneField,
)

from crypto.managers.quotes import QuoteManager
from crypto.models import Quote
from utils.enums import TimeUnits


class Distance(Model):
    mm7 = FloatField(max_length=128, verbose_name="mm7", null=True)
    mm20 = FloatField(max_length=128, verbose_name="mm20", null=True)
    mm50 = FloatField(max_length=128, verbose_name="mm50", null=True)
    mm100 = FloatField(max_length=128, verbose_name="mm100", null=True)
    mm200 = FloatField(max_length=128, verbose_name="mm200", null=True)
    support = FloatField(max_length=128, verbose_name="support")
    resistance = FloatField(max_length=128, verbose_name="resistance")
    quote: Quote = OneToOneField(
        "crypto.Quote",
        related_name="distances",
        max_length=128,
        null=True,
        on_delete=SET_NULL,
    )

    def __str__(self):
        return f"Distance {self.quote}"

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

    class Meta:
        constraints = (UniqueConstraint(fields=("quote",), name="unique_per_quote"),)
