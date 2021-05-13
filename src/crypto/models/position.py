from django.db import models

from crypto.utils.enums import PositionStatus


class Position(models.Model):
    symbol = models.OneToOneField(
        "crypto.Symbol",
        verbose_name="symbol",
        related_name="positions",
        on_delete=models.SET_NULL,
        null=True,
    )
    date = models.DateField()
    nb_titres = models.IntegerField()
    pru = models.FloatField()
    status = models.CharField(max_length=128, choices=PositionStatus.choices)

    portfolio = models.ForeignKey(
        "crypto.Portfolio",
        verbose_name="portfolio",
        related_name="positions",
        on_delete=models.CASCADE,
        null=True,
    )

    @property
    def size(self) -> float:
        return self.pru * self.nb_titres

    def amount(self, current_price: float) -> float:
        return current_price * self.nb_titres
