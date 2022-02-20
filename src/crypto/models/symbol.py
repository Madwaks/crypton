from datetime import datetime
from functools import cached_property
from typing import TYPE_CHECKING

import numpy as np
from django.contrib.postgres.fields import ArrayField
from django.db.models import (
    CharField,
    UniqueConstraint,
    OneToOneField,
    SET_NULL,
    Manager,
)

from crypto.managers.last_quote import LastQuoteManager
from crypto.models.abstract import AbstractModel
from utils.enums import TimeUnits

if TYPE_CHECKING:
    from crypto.models import Quote


class Symbol(AbstractModel):
    name = CharField(max_length=20)
    base_asset = CharField(max_length=10)
    quote_asset = CharField(max_length=10)
    order_types = ArrayField(
        base_field=CharField(max_length=64, null=True), size=10, null=True, blank=True
    )
    objects = Manager()
    last_quotes = LastQuoteManager()

    def __str__(self) -> CharField:
        return self.name

    def is_up_to_date(self, time_unit: TimeUnits) -> bool:
        last_quote = self.get_last_quote(time_unit)
        if last_quote:
            start_ = last_quote.close_date
            return (start_ + time_unit.to_timedelta()) > datetime.utcnow()
        return False

    def get_last_quote(self, time_unit: TimeUnits):
        return self.quotes.get_last_quote_by_time_unit(time_unit)

    @cached_property
    def next_supp(self):
        key_levels, difference_close = self.distances_to_key_levels
        supp_array = np.array([diff for diff in difference_close if diff <= 0])

        diff_supp = supp_array[supp_array.argmax()] if supp_array.any() else None
        return key_levels[np.where(difference_close == diff_supp)][0]

    @cached_property
    def next_res(self) -> tuple[float, float]:
        key_levels, difference_close = self.distances_to_key_levels

        res_array = np.array([diff for diff in difference_close if diff > 0])

        diff_res = res_array[res_array.argmin()] if res_array.any() else None

        return key_levels[np.where(difference_close == diff_res)][0]

    @cached_property
    def distances_to_key_levels(self):
        key_levels = np.array(self.indicators.values_list("value", flat=True))
        return key_levels, key_levels - self.last_close

    class Meta:
        verbose_name = "Symbol"
        verbose_name_plural = "Symbols"
        ordering = ("name", "base_asset", "quote_asset")
        constraints = (
            UniqueConstraint(
                fields=("name", "base_asset", "quote_asset"),
                name="unique_per_symbol_pairs",
            ),
        )
