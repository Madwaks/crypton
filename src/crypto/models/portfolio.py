from typing import TypeVar, TYPE_CHECKING

from django.db import models

from crypto.models import Position
from crypto.utils.enums import Side

if TYPE_CHECKING:
    from crypto.models import Symbol
    from crypto.models.order import Order

    OrderType = TypeVar("OrderType", bound=Order)


class Portfolio(models.Model):
    solde = models.FloatField()

    @property
    def buy_positions(self):
        return self.positions.filter(side=Side.BUY)

    @property
    def sell_positions(self):
        return self.positions.filter(side=Side.SELL)

    def available_titres_for_symbol(self, symbol: "Symbol"):
        bought = sum(
            [pos.nb_titres for pos in self.buy_positions.filter(symbol=symbol)]
        )
        sold = sum([pos.nb_titres for pos in self.sell_positions.filter(symbol=symbol)])
        return bought - sold

    def open_position(self, order: "OrderType") -> Position:
        position = Position.from_order(order, self)
        self._add_position(position)

        return position

    def get_nb_titres_to_buy(self, price: float):
        return (0.20 * self.solde) / price

    def update_solde(self, value: float):
        setattr(self, "solde", self.solde + value)

    def close_position(self, order: "OrderType") -> Position:
        position = Position.from_order(order, self)
        self._remove_position(position)

        return position

    def _add_position(self, position: Position):
        if self.solde - position.size < 0:
            raise Exception("Insufficient amount in the portfolio")
        self.positions.add(position, bulk=False)
        # self.update_solde_titre(position.amount(position.pru))
        self.update_solde(-position.size)

    def _remove_position(self, position: Position):
        if self.available_titres_for_symbol(position.symbol) < position.nb_titres:
            raise Exception("Insufficient shares in portfolio")
        self.positions.add(position, bulk=False)
        self.update_solde(position.size)
