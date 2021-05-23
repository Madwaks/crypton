from datetime import datetime
from logging import getLogger

from injector import singleton, inject

from crypto.models import Symbol, Quote
from decision_maker.models import Indicator
from decision_maker.models.enums import AvailableIndicators
from decision_maker.utils.etc import is_quote_in_tolerance_range
from utils.enums import TimeUnits
import numpy as np


@singleton
class Backtester:
    @inject
    def __init__(self):
        self._logger = getLogger("django")

    def apply_to_symbol(self, symbol: Symbol, time_unit: TimeUnits):
        quotes: list[Quote] = symbol.quotes.filter(time_unit=time_unit.value).order_by(
            "timestamp"
        )

        tolerance = 0.005

        for current_quote in quotes:
            if current_quote.open_date < datetime(year=2021, month=1, day=1):
                continue
            key_levels = np.array(
                current_quote.symbol.indicators.values_list("value", flat=True)
            )
            near_res, near_supp = self._find_nearest_supp_and_res(
                current_quote, key_levels
            )
            slope_states = self._get_indicators_states(current_quote)

            wanted_states: dict[AvailableIndicators, bool] = {
                AvailableIndicators.MM7: True
            }

            next_quote = Quote.objects.get_next_quote(current_quote)

            for state in wanted_states.keys():
                if slope_states[state] > 0 and (
                    is_quote_in_tolerance_range(
                        current_quote.close, near_supp, tolerance
                    )
                ):
                    self._logger.info(f"Order BUY sent: {next_quote.open_date}")
                    # self._send_order(next_quote)

    def _get_indicators_states(self, quote: Quote):
        indicators: list[Indicator] = quote.indicators.all().order_by("name")
        previous = Quote.objects.get_previous_quote(quote)
        previous_indicators: list[Indicator] = previous.indicators.all().order_by(
            "name"
        )

        slope_states: dict[AvailableIndicators, float] = dict()

        for prev_ind, ind in zip(previous_indicators, indicators):
            slope_states[
                AvailableIndicators.from_code(prev_ind.name)
            ] = self._get_slope_state(prev_ind, ind)

        return slope_states

    def _get_slope_state(self, prev_val: Indicator, val: Indicator) -> float:
        assert prev_val.name == val.name
        return val - prev_val

    def _find_nearest_supp_and_res(
        self, quote: Quote, key_levels: "np.ndarray"
    ) -> tuple[float, float]:

        difference_close = key_levels - quote.close

        supp_array = np.array([diff for diff in difference_close if diff <= 0])
        res_array = np.array([diff for diff in difference_close if diff > 0])

        diff_res = res_array[res_array.argmin()] if res_array.any() else None
        diff_supp = supp_array[supp_array.argmax()] if supp_array.any() else None
        return (
            key_levels[np.where(difference_close == diff_res)][0],
            key_levels[np.where(difference_close == diff_supp)][0],
        )
