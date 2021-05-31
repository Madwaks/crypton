from collections import Counter

from injector import singleton, inject
from crypto.models import Quote
from crypto.utils.enums import Side
from decision_maker.models import QuoteState
from decision_maker.services.repositories.indicator import IndicatorStateRepository
from decision_maker.utils.etc import is_in_tolerance_range

tolerance = 0.005


@singleton
class StrategyFactory:
    @inject
    def __init__(self, indicator_repository: IndicatorStateRepository):
        self._ind_state_repo = indicator_repository

    def _get_decision_for_quote(self, quote: Quote):

        nb_buy_signals = self._get_buy_signals(quote)
        nb_sell_signals = self._get_sell_signals(quote)
        if nb_buy_signals > nb_sell_signals:
            return Side.BUY
        else:
            return Side.SELL

    def _get_buy_signals(self, quote: Quote) -> int:
        quote_state: QuoteState = QuoteState.objects.get(quote=quote)
        buy_signals_count = 0
        if quote_state.mean > 0:
            buy_signals_count += 1

        near_res, near_supp = self._ind_state_repo.find_nearest_supp_and_res(quote)

        indicators_on_support = [
            is_in_tolerance_range(indicator.value, near_supp, tolerance)
            for indicator in quote.indicators.filter(name__startswith="MM")
        ]
        buy_signals_count += Counter(indicators_on_support)[True]

        candlestick_on_support = any(
            [
                is_in_tolerance_range(getattr(quote, field), near_supp, tolerance)
                for field in ["open", "close", "high", "low"]
            ]
        )
        if candlestick_on_support:
            buy_signals_count += 1

        return buy_signals_count

    def _get_sell_signals(self, quote: Quote) -> int:
        quote_state: QuoteState = QuoteState.objects.get(quote=quote)
        sell_signals_count = 0
        if quote_state.mean < 0:
            sell_signals_count += 1

        near_res, near_supp = self._ind_state_repo.find_nearest_supp_and_res(quote)

        indicators_on_support = [
            is_in_tolerance_range(indicator.value, near_res, tolerance)
            for indicator in quote.indicators.filter(name__startswith="MM")
        ]
        sell_signals_count += Counter(indicators_on_support)[False]

        candlestick_on_res = [
            is_in_tolerance_range(getattr(quote, field), near_supp, tolerance)
            for field in ["open", "close", "high", "low"]
        ]
        sell_signals_count += Counter(candlestick_on_res)[False]

        return sell_signals_count
