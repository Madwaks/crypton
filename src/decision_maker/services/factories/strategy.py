from typing import Optional

from injector import singleton, inject
from crypto.models import Quote
from crypto.utils.enums import Side
from decision_maker.services.repositories.indicator import IndicatorStateRepository
from decision_maker.utils.etc import is_in_tolerance_range

tolerance = 0.0005


@singleton
class StrategyFactory:
    @inject
    def __init__(self, indicator_repository: IndicatorStateRepository):
        self._ind_state_repo = indicator_repository

    def _get_decision_for_quote(
        self, previous_quote: Quote, quote: Quote
    ) -> Optional[Side]:
        near_res, near_supp = self._ind_state_repo.find_nearest_supp_and_res(
            previous_quote
        )
        previous_mm7 = previous_quote.indicators.get(name="MM7").value
        mm7 = quote.indicators.get(name="MM7").value
        if (
            any(
                [
                    is_in_tolerance_range(candle, near_supp)
                    for candle in [
                        previous_quote.close,
                        previous_quote.open,
                        previous_quote.high,
                        previous_quote.low,
                    ]
                ]
            )
            and previous_mm7 < mm7
        ):
            return Side.BUY
        elif any(
            [
                is_in_tolerance_range(candle, near_res)
                for candle in [
                    previous_quote.close,
                    previous_quote.open,
                    previous_quote.high,
                    previous_quote.low,
                ]
            ]
        ):
            return Side.SELL
