from datetime import timedelta

from dateutil.relativedelta import relativedelta
from django.db.models import TextChoices


class TimeUnits(TextChoices):
    minutes1 = "1m"
    minutes5 = "5m"
    minutes15 = "15m"
    minutes30 = "30m"
    HOUR1 = "1h"
    HOUR4 = "4h"
    DAY1 = "1d"
    WEEK1 = "1w"
    MONTH1 = "1M"

    @classmethod
    def from_code(cls, code: str):
        for c_type in cls:
            if c_type.value == code:
                return c_type
        return None

    @property
    def minutes_interval(self):
        return self.time_to_minutes.get(self)

    @property
    def time_to_minutes(self):
        return {
            self.minutes1.value: 1,
            self.minutes5.value: 5,
            self.minutes15.value: 15,
            self.minutes30.value: 30,
            self.HOUR1.value: 60,
            self.HOUR4.value: 240,
            self.DAY1.value: 1440,
            self.WEEK1.value: 10080,
            self.MONTH1.value: None,
        }

    @property
    def timedelta_mapping(self):
        return {
            self.minutes1.value: timedelta(minutes=1),
            self.minutes5.value: timedelta(minutes=5),
            self.minutes15.value: timedelta(minutes=15),
            self.minutes30.value: timedelta(minutes=30),
            self.HOUR1.value: timedelta(hours=1),
            self.HOUR4.value: timedelta(hours=4),
            self.DAY1.value: timedelta(days=1),
            self.WEEK1.value: timedelta(weeks=1),
            self.MONTH1.value: relativedelta(month=1),
        }

    def to_timedelta(self):
        return self.timedelta_mapping[self.value]
