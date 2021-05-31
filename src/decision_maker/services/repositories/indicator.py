from injector import singleton, inject
import numpy as np
from crypto.models import Quote
from decision_maker.models import Indicator
from decision_maker.models.enums import AvailableIndicators


@singleton
class IndicatorStateRepository:
    @inject
    def __init__(self):
        pass

    def get_indicators_slopes(self, quote: Quote):
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

    @staticmethod
    def find_nearest_supp_and_res(quote: Quote) -> tuple[float, float]:
        key_levels = np.array(quote.symbol.indicators.values_list("value", flat=True))
        difference_close = key_levels - quote.close

        supp_array = np.array([diff for diff in difference_close if diff <= 0])
        res_array = np.array([diff for diff in difference_close if diff > 0])

        diff_res = res_array[res_array.argmin()] if res_array.any() else None
        diff_supp = supp_array[supp_array.argmax()] if supp_array.any() else None
        return (
            key_levels[np.where(difference_close == diff_res)][0],
            key_levels[np.where(difference_close == diff_supp)][0],
        )
