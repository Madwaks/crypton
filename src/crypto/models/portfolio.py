from django.db import models

from crypto.models import Symbol
from crypto.utils.enums import Side


class Portfolio(models.Model):
    initial_solde = models.FloatField()

    @property
    def solde(self) -> float:
        return (
            self.initial_solde
            - sum([pos.size for pos in self.buy_positions])
            + sum([pos.size for pos in self.sell_positions])
        )

    @property
    def buy_positions(self):
        return self.positions.filter(side=Side.BUY)

    @property
    def sell_positions(self):
        return self.positions.filter(side=Side.SELL)

    def available_titres_for_symbol(self, symbol: Symbol):
        return sum([pos.nb_titres for pos in self.buy_positions.filter(symbol=symbol)])
