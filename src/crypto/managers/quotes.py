from typing import TYPE_CHECKING

from django.db.models import Manager
from django.db.models.query import QuerySet
from pandas import DataFrame


if TYPE_CHECKING:
    from crypto.models import Pair, Symbol


class QuoteManager(Manager):
    def get_as_dataframe(self) -> DataFrame:
        return DataFrame(list(self.all().values()))

    def get_last_company_quote(self, symbol: "Symbol") -> "QuerySet":
        return self.filter(symbol=symbol).latest("date")

    def get_last_pair_quote(self, pair: "Pair"):
        return self.filter(pair=pair).latest("timestamp")
