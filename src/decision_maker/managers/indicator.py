from typing import TYPE_CHECKING

from django.db.models import Manager

if TYPE_CHECKING:
    from crypto.models import Symbol


class IndicatorManager(Manager):
    def get_last_indicators_for_symbol(self, symbol: "Symbol"):
        for ind in self.all():
            if ind.quote.symbol == symbol:
                pass

        return self.filter()

    def get_dict_states(self):
        return self.filter()
