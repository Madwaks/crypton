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
    def binsize(self):
        return self.time_to_binsize[self.value]

    @property
    def time_to_binsize(self):
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
