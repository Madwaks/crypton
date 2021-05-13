from django.db import models

from crypto.models import Symbol, Position


class Portfolio(models.Model):
    solde = models.FloatField()

    def open_position(self, symbol: Symbol, timestamp: int, nb_titres: int, pru: float):
        position = self.positions.create(
            timestamp=timestamp,
            symbol=symbol,
            status="OPEN",
            nb_titres=nb_titres,
            pru=pru,
        )
        self._update_solde(-position.amount(pru))

    def close_position(self, position: Position, price: float):
        self.positions.status = "CLOSED"
        self._update_solde(position.amount(price))

    def _update_solde(self, value: float):
        self.solde += value
