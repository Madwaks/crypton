from logging import getLogger
from time import time
from typing import NoReturn, Union

from django.db.models import QuerySet
from injector import singleton, inject

from crypto.models import Symbol, Quote
from decision_maker.models import Indicator, SymbolIndicator
from decision_maker.models.distance import Distance
from decision_maker.services.factories.key_level import KeyLevelFactory
from decision_maker.utils.indicators.distance import DistanceFactory
from decision_maker.utils.indicators.moving_average import MovingAverageIndicatorFactory
from utils.enums import TimeUnits

logger = getLogger("django")


@singleton
class IndicatorComputer:
    @inject
    def __init__(
        self,
        moving_average_factory: MovingAverageIndicatorFactory,
        key_levels_factory: KeyLevelFactory,
        distance_factory: DistanceFactory,
    ):
        self._key_level_factory = key_levels_factory
        self._distance_factory = distance_factory
        self._moving_average_factory = moving_average_factory

    def compute_indicators_for_symbol(
        self, symbol: Union[str, Symbol], time_unit: TimeUnits
    ) -> NoReturn:

        if isinstance(symbol, str):
            symbol = Symbol.objects.get(name=symbol)

        quotes = symbol.quotes.get_symbol_and_tu_quotes(
            time_unit=time_unit
        ).prefetch_related("indicators")
        if quotes.exists():

            self._compute_symbol_indicators(symbol, time_unit, quotes)

            self._compute_moving_average(quotes)

            self._compute_quote_to_ind_distances(quotes)

    def _compute_moving_average(self, quotes):
        indicators = self._moving_average_factory.build_moving_average_indicators(
            quotes
        )
        self._save_indicators(indicators)
        logger.info(
            f"[Indicators] Stored {len(indicators)} moving average values for {quotes.first().symbol}"
        )

    def _compute_quote_to_ind_distances(self, quotes: QuerySet[Quote]) -> NoReturn:
        distances = self._distance_factory.build_distances(quotes)
        self._save_distances(distances)
        logger.info(
            f"[Distances] Stored {len(distances)} distances values for {quotes.first().symbol}"
        )

    def _compute_symbol_indicators(
        self, symbol: Symbol, time_unit: TimeUnits, quotes: QuerySet[Quote]
    ) -> NoReturn:
        if not symbol.indicators.exists():
            symbol_indicators = self._key_level_factory.build_key_level_for_symbol(
                symbol, time_unit, quotes
            )
            self._save_symbol_indicators(symbol_indicators)
            logger.info(
                f"[Indicators] Stored {len(symbol_indicators)} key levels values for {symbol}"
            )

    @staticmethod
    def _save_indicators(indicator_list: list[Indicator]) -> NoReturn:
        Indicator.objects.bulk_create(indicator_list)

    @staticmethod
    def _save_symbol_indicators(indicator_list: list[SymbolIndicator]) -> NoReturn:
        SymbolIndicator.objects.bulk_create(indicator_list)

    @staticmethod
    def _save_distances(distance_list: list[Distance]):
        Distance.objects.bulk_create(distance_list)
