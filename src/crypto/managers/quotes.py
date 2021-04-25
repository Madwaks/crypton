from typing import TYPE_CHECKING, Optional

from django.db.models import Manager
from django.db.models.query import QuerySet
from pandas import DataFrame

from utils.enums import TimeUnits

if TYPE_CHECKING:
    from crypto.models import Pair, Symbol


class QuoteManager(Manager):
    def get_as_dataframe(self, time_unit: Optional[TimeUnits] = None) -> DataFrame:
        if time_unit:
            return DataFrame(list(self.filter(time_unit=time_unit).values()))
        return DataFrame(list(self.all().values()))

    def get_last_company_quote(self, symbol: "Symbol") -> "QuerySet":
        return self.filter(symbol=symbol).latest("date")

    def get_last_pair_quote(self, pair: "Pair"):
        return self.filter(pair=pair).latest("timestamp")
