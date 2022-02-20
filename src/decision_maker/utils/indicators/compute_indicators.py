from logging import getLogger
from time import time
from typing import NoReturn, Union, Optional

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
        self, symbol: Union[str, Symbol], time_unit: TimeUnits, save: bool = True
    ) -> NoReturn:

        if isinstance(symbol, str):
            symbol = Symbol.objects.get(name=symbol)

        quotes = symbol.quotes.get_symbol_and_tu_quotes(
            time_unit=time_unit
        ).prefetch_related("indicators")
        if quotes.exists() and quotes.count() >= 720:
            self._compute_symbol_indicators(symbol, time_unit, quotes, save)

            self._compute_moving_average(quotes, symbol, save)

            self._compute_quote_to_ind_distances(quotes, symbol, save)

    def _compute_moving_average(
        self, quotes, symbol: Symbol, save: bool = True
    ) -> Optional[list]:
        indicators = self._moving_average_factory.build_moving_average_indicators(
            quotes
        )
        if save:
            return self._save_indicators(indicators, symbol)
        return indicators

    def _compute_quote_to_ind_distances(
        self, quotes: QuerySet[Quote], symbol: Symbol, save: bool = True
    ) -> Optional[list]:
        distances = self._distance_factory.build_distances(quotes)
        if save:
            return self._save_distances(distances, symbol)
        return distances

    def _compute_symbol_indicators(
        self,
        symbol: Symbol,
        time_unit: TimeUnits,
        quotes: QuerySet[Quote],
        save: bool = True,
    ) -> NoReturn:
        if not symbol.indicators.filter(time_unit=time_unit.value).exists():
            symbol_indicators = self._key_level_factory.build_key_level_for_symbol(
                symbol, time_unit, quotes
            )
            if save:
                self._save_symbol_indicators(symbol_indicators, symbol)
            return symbol_indicators

    @staticmethod
    def _save_indicators(indicator_list: list[Indicator], symbol: Symbol) -> NoReturn:
        Indicator.objects.bulk_create(indicator_list)
        logger.info(
            f"[Indicators] Stored {len(indicator_list)} moving average values for {symbol.name}"
        )

    @staticmethod
    def _save_symbol_indicators(
        indicator_list: list[SymbolIndicator], symbol: Symbol
    ) -> NoReturn:
        SymbolIndicator.objects.bulk_create(indicator_list)
        logger.info(
            f"[Indicators] Stored {len(indicator_list)} key levels values for {symbol.name}"
        )

    @staticmethod
    def _save_distances(distance_list: list[Distance], symbol: Symbol):
        Distance.objects.bulk_create(distance_list)
        logger.info(
            f"[Distances] Stored {len(distance_list)} distances values for {symbol.name}"
        )
