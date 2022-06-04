from logging import getLogger
from typing import TYPE_CHECKING, Optional

from django.db.models import Manager
from django.db.models.query import QuerySet
from numpy import var, mean
from pandas import DataFrame

from decision_maker.utils.etc import get_timestamp_diff_unit
from utils.enums import TimeUnits

if TYPE_CHECKING:
    from crypto.models import Symbol, Quote

logger = getLogger()


class QuoteManager(Manager):
    def get_previous_quote(self, quote: "Quote") -> "Quote":
        try:
            return self.get(pk=get_timestamp_diff_unit(quote=quote, diff_number=1))
        except self.model.DoesNotExist:
            logger.warning(f"{quote.open_date} is the last quote i got in my DB!")
            return None

    def get_next_quote(self, quote: "Quote") -> "Quote":
        try:
            return self.get(pk=get_timestamp_diff_unit(quote=quote, diff_number=-1))
        except self.model.DoesNotExist:
            logger.warning(f"{quote.open_date} is the last quote i got in my DB!")
            return None

    def get_as_dataframe(
        self, time_unit: TimeUnits, symbol: Optional["Symbol"] = None
    ) -> DataFrame:

        return DataFrame(
            list(self.get_symbol_and_tu_quotes(time_unit, symbol).values())
        )

    def get_symbol_and_tu_quotes(
        self, time_unit: TimeUnits, symbol: Optional["Symbol"] = None
    ) -> QuerySet:
        if symbol:
            return self.filter(symbol=symbol, time_unit=time_unit)
        return self.filter(time_unit=time_unit).order_by("-timestamp")

    def get_last_quotes(self):
        return self.order_by("time_unit", "-timestamp").distinct("time_unit")

    def get_last_quote_by_time_unit(self, time_unit: TimeUnits):
        return self.get_last_quotes().filter(time_unit=time_unit.value).first()

    def get_max_close(self, time_unit: TimeUnits) -> float:
        return max(
            self.filter(time_unit=time_unit.value).values_list("close", flat=True)
        )

    def get_min_close(self, time_unit: TimeUnits) -> float:
        return min(
            self.filter(time_unit=time_unit.value).values_list("close", flat=True)
        )

    def get_variance(self, nb_previous: int, time_unit: TimeUnits):
        return var(
            self.get_symbol_and_tu_quotes(time_unit)
            .only("close")[nb_previous:]
            .values_list("close", flat=True)
        )

    def get_mean_volume(self, nb_previous: int, time_unit: TimeUnits):
        return mean(
            self.get_symbol_and_tu_quotes(time_unit)
            .only("volume")[nb_previous:]
            .values_list("volume", flat=True)
        )

    def get_mean_price(self, nb_previous: int, time_unit: TimeUnits):
        return mean(
            self.get_symbol_and_tu_quotes(time_unit)
            .only("close")[nb_previous:]
            .values_list("close", flat=True)
        )
