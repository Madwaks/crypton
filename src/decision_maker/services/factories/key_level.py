from collections import Counter

import numpy as np
from injector import singleton
from pandas import DataFrame, Series
from sklearn.cluster import KMeans
from tqdm import tqdm

from crypto.models import Symbol
from decision_maker.models import SymbolIndicator
from utils.enums import TimeUnits


@singleton
class KeyLevelFactory:
    window_size: int = 100
    nb_digits: int = 2
    center: bool = False
    closed: str = "left"

    def build_key_level_for_symbol(
        self, symbol: Symbol, time_unit: TimeUnits
    ) -> list[SymbolIndicator]:

        quotes: DataFrame = symbol.quotes.get_as_dataframe(time_unit=time_unit)

        prices = self._get_price_counter(quotes)
        best_kmeans = self._find_best_kmeans(prices)

        key_levels = list(best_kmeans.cluster_centers_.flatten())

        return self._build_symbol_indicator_from_levels(
            symbol=symbol, time_unit=time_unit, key_levels=key_levels
        )

    def _get_price_counter(self, quotes: DataFrame) -> list[float]:
        min_lows, max_lows = self._get_rolling_min_max(quotes, "low")
        min_opens, max_opens = self._get_rolling_min_max(quotes, "open")
        min_highs, max_highs = self._get_rolling_min_max(quotes, "high")
        min_closes, max_closes = self._get_rolling_min_max(quotes, "close")
        counter_level = Counter(min_lows)
        counter_level.update(Counter(max_lows))

        counter_level.update(Counter(min_opens))
        counter_level.update(Counter(max_opens))

        counter_level.update(Counter(min_highs))
        counter_level.update(Counter(max_highs))

        counter_level.update(Counter(min_closes))
        counter_level.update(Counter(max_closes))

        counter_level = {
            price: counter for price, counter in counter_level.items() if counter >= 100
        }
        return list(counter_level.keys())

    def _get_rolling_min_max(
        self, quotes_df: DataFrame, column_name: str
    ) -> tuple[Series, Series]:
        rolling_df: Series = quotes_df[column_name].map(
            lambda val: round(val, 6)
        ).rolling(self.window_size, center=self.center, closed=self.closed)
        return rolling_df.min().dropna(), rolling_df.max().dropna()

    @staticmethod
    def _find_best_kmeans(prices: list[float]) -> KMeans:
        kmeans_results: dict[float, KMeans] = dict()
        for n_cluster in range(5, int(len(prices) + 1 / 2)):
            kmeans = KMeans(n_clusters=n_cluster)
            kmeans.fit(np.array(prices).reshape(-1, 1))
            kmeans_results[kmeans.inertia_] = kmeans
        return kmeans_results[min(kmeans_results)]

    def _build_symbol_indicator_from_levels(
        self, symbol: Symbol, time_unit: TimeUnits, key_levels: list[float]
    ) -> list[SymbolIndicator]:
        list_sind = []
        for i, level in tqdm(enumerate(sorted(key_levels))):
            s_ind = SymbolIndicator(
                name=f"KeyLevel{i}", value=level, symbol=symbol, time_unit=time_unit
            )
            list_sind.append(s_ind)
        return list_sind
