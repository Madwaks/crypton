from typing import TYPE_CHECKING

import numpy as np
from injector import singleton, inject

from utils.enums import TimeUnits

if TYPE_CHECKING:
    from crypto.models import Quote
from decision_maker.models import Indicator
from decision_maker.models.enums import AvailableIndicators


def find_nearest_supp_and_res(quote: "Quote") -> tuple[float, float]:
    key_levels = np.array(
        quote.symbol.indicators.filter(time_unit=quote.time_unit).values_list(
            "value", flat=True
        )
    )
    key_levels = np.append(
        key_levels,
        [
            quote.symbol.quotes.get_max_close(TimeUnits.from_code(quote.time_unit)),
            quote.symbol.quotes.get_min_close(TimeUnits.from_code(quote.time_unit)),
        ],
    )
    difference_close = key_levels - quote.close
    next_res_diff = min([diff for diff in difference_close if diff > 0])
    next_supp_diff = min([diff for diff in difference_close if diff < 0])

    return (
        key_levels[np.where(difference_close == next_res_diff)][0],
        key_levels[np.where(difference_close == next_supp_diff)][0],
    )


@singleton
class IndicatorStateRepository:
    @inject
    def __init__(self):
        pass

    def get_indicators_slopes(self, quote: "Quote"):
        indicators: list[Indicator] = quote.indicators.all().order_by("name")
        previous = Quote.objects.get_previous_quote(quote)
        if previous is None:
            return None
        previous_indicators: list[Indicator] = previous.indicators.all().order_by(
            "name"
        )

        slope_states: dict[AvailableIndicators, float] = dict()

        for prev_ind, ind in zip(previous_indicators, indicators):
            slope_states[
                AvailableIndicators.from_code(prev_ind.name)
            ] = self._get_slope(prev_ind, ind)

        return slope_states

    @staticmethod
    def _get_slope(prev_ind: "Indicator", ind: "Indicator") -> float:
        assert prev_ind.name == ind.name
        return ind.value - prev_ind.value
