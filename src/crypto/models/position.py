from django.db import models
from django.db.models import UniqueConstraint

from crypto.models import Portfolio
from crypto.models.order import Order
from crypto.utils.enums import Side


class Position(models.Model):
    timestamp = models.CharField(max_length=256, default="", primary_key=True)
    symbol = models.ForeignKey(
        "crypto.Symbol",
        verbose_name="symbol",
        related_name="positions",
        on_delete=models.CASCADE,
        null=True,
    )
    nb_titres = models.FloatField()
    pru = models.FloatField()
    side = models.CharField(max_length=128, choices=Side.choices, default=Side.BUY)

    portfolio = models.ForeignKey(
        "crypto.Portfolio",
        verbose_name="portfolio",
        related_name="positions",
        on_delete=models.CASCADE,
        null=True,
    )

    @classmethod
    def from_order(cls, order: Order, portfolio: Portfolio, price: float):
        return cls(
            timestamp=order.timestamp,
            portfolio=portfolio,
            side=order.side,
            symbol=order.symbol,
            nb_titres=order.quantity,
            pru=price,
        )

    @property
    def size(self) -> float:
        return self.pru * self.nb_titres

    def amount(self, current_price: float) -> float:
        return current_price * self.nb_titres

    def save(self, **kwargs):
        portfolio = self.portfolio
        if portfolio and portfolio.pk is None:
            portfolio.save()

        self.portfolio = portfolio

        super().save(**kwargs)

    class Meta:
        verbose_name = "Position"
        verbose_name_plural = "Positions"
        constraints = (
            UniqueConstraint(
                fields=("timestamp", "symbol", "portfolio"),
                name="unique_per_ts_symbol_and_portfolio",
            ),
        )
