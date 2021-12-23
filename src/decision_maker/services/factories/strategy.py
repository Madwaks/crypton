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
        if self._candle_near_key_level(quote, near_supp):
            return Side.BUY
        elif self._candle_near_key_level(quote, near_res):
            return Side.SELL

    def _candle_near_key_level(self, quote: Quote, key_level: float) -> bool:
        return any(
            [
                is_in_tolerance_range(candle, key_level)
                for candle in [quote.close, quote.open, quote.high, quote.low]
            ]
        )
