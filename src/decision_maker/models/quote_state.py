from django.db.models import Model, FloatField, OneToOneField, CASCADE
from numpy.core import mean


class QuoteState(Model):
    quote = OneToOneField(
        "crypto.Quote",
        related_name="quote_state",
        null=False,
        blank=False,
        on_delete=CASCADE,
    )

    MM7_MM20: float = FloatField(default=0.0)
    MM7_MM50: float = FloatField(default=0.0)
    MM7_MM100: float = FloatField(default=0.0)
    MM7_MM200: float = FloatField(default=0.0)
    PRICE_MM7: float = FloatField(default=0.0)
    MM20_MM50: float = FloatField(default=0.0)
    MM20_MM100: float = FloatField(default=0.0)
    MM20_MM200: float = FloatField(default=0.0)
    PRICE_MM20: float = FloatField(default=0.0)
    MM50_MM100: float = FloatField(default=0.0)
    MM50_MM200: float = FloatField(default=0.0)
    PRICE_MM50: float = FloatField(default=0.0)
    MM100_MM200: float = FloatField(default=0.0)
    PRICE_MM100: float = FloatField(default=0.0)
    PRICE_MM200: float = FloatField(default=0.0)

    @property
    def mean(self) -> float:
        return mean(
            [
                getattr(self, field.name)
                for field in self._meta.fields
                if field.name not in ["id", "quote"]
            ]
        )
