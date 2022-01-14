from datetime import datetime

from django.db.models import (
    Model,
    FloatField,
    SET_NULL,
    UniqueConstraint,
    OneToOneField,
)

from crypto.models import Quote


class Distance(Model):
    MM7 = FloatField(max_length=128, verbose_name="mm7", null=True)
    MM20 = FloatField(max_length=128, verbose_name="mm20", null=True)
    MM50 = FloatField(max_length=128, verbose_name="mm50", null=True)
    MM100 = FloatField(max_length=128, verbose_name="mm100", null=True)
    MM200 = FloatField(max_length=128, verbose_name="mm200", null=True)
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
