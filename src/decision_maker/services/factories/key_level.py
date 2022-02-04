from collections import Counter
from dataclasses import dataclass

import numpy as np
from django.db.models import QuerySet
from injector import singleton, inject
from pandas import DataFrame, Series
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from tqdm import tqdm

from crypto.models import Symbol, Quote
from decision_maker.models import SymbolIndicator
from utils.enums import TimeUnits


@singleton
class KeyLevelFactory:
    @dataclass
    class Configuration:
        window_size: int = 100
        nb_digits: int = 2
        center: bool = False
        closed: str = "left"

    @inject
    def __init__(self, config: Configuration):
        self._config = config

    def build_key_level_for_symbol(
        self, symbol: Symbol, time_unit: TimeUnits, quotes: QuerySet[Quote]
    ) -> list[SymbolIndicator]:

        quotes: DataFrame = DataFrame(list(quotes.values()))
        higher_res = quotes[["open", "high", "low", "close"]].max().max()
        lower_supp = quotes[["open", "high", "low", "close"]].min().min()
        prices = self._get_price_counter(quotes)
        best_kmeans = self._find_best_kmeans(prices)

        if best_kmeans:
            key_levels = list(best_kmeans.cluster_centers_.flatten())

            key_levels += [higher_res, lower_supp]

            return self._build_symbol_indicator_from_levels(
                symbol=symbol, time_unit=time_unit, key_levels=key_levels
            )
        return []

    def _get_max_clusters(self, prices: list) -> int:
        return int((len(prices) + 1) / 2)

    def _get_price_counter(self, quotes: DataFrame) -> list[float]:

        counter_level = Counter()
        min_lows, max_lows = self._get_rolling_min_max(quotes, "low")
        counter_level.update(Counter(min_lows))
        counter_level.update(Counter(max_lows))

        min_highs, max_highs = self._get_rolling_min_max(quotes, "high")
        counter_level.update(Counter(min_highs))
        counter_level.update(Counter(max_highs))

        min_opens, max_opens = self._get_rolling_min_max(quotes, "open")
        counter_level.update(Counter(min_opens))
        counter_level.update(Counter(max_opens))

        min_closes, max_closes = self._get_rolling_min_max(quotes, "close")
        counter_level.update(Counter(min_closes))
        counter_level.update(Counter(max_closes))

        counter_level = {
            price: counter for price, counter in counter_level.items() if counter >= 100
        }

        return list(counter_level.keys())

    def _get_rolling_min_max(
        self, quotes_df: DataFrame, column_name: str
    ) -> tuple[Series, Series]:
        rolling_df: Series = quotes_df[column_name].rolling(
            window=self._config.window_size,
            center=self._config.center,
            closed=self._config.closed,
        )
        return rolling_df.min().dropna(), rolling_df.max().dropna()

    def _find_best_kmeans(self, prices: list[float]) -> KMeans:
        kmeans_results: dict[float, KMeans] = dict()
        array = np.array(prices).reshape(-1, 1)
        max_clusters = self._get_max_clusters(prices)
        for n_cluster in range(5, max_clusters):
            kmeans = KMeans(n_clusters=n_cluster)
            kmeans.fit(array)
            labels = kmeans.fit_predict(array)
            silhouette = silhouette_score(array, labels)
            kmeans_results[silhouette] = kmeans
        return kmeans_results[max(kmeans_results)]

    def _build_symbol_indicator_from_levels(
        self, symbol: Symbol, time_unit: TimeUnits, key_levels: list[float]
    ) -> list[SymbolIndicator]:
        list_sind = []
        for i, level in enumerate(sorted(key_levels), 1):
            s_ind = SymbolIndicator(
                name=f"KeyLevel{i}", value=level, symbol=symbol, time_unit=time_unit
            )
            list_sind.append(s_ind)
        return list_sind
