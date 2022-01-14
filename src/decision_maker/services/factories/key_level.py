from collections import Counter

import numpy as np
from django.db.models import QuerySet
from injector import singleton
from pandas import DataFrame, Series
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from tqdm import tqdm

from crypto.models import Symbol, Quote
from decision_maker.models import SymbolIndicator
from utils.enums import TimeUnits


@singleton
class KeyLevelFactory:
    window_size: int = 100
    nb_digits: int = 2
    center: bool = False
    closed: str = "left"

    def build_key_level_for_symbol(
        self,
        symbol: Symbol,
        time_unit: TimeUnits,
        quotes_for_symbol_and_tu: QuerySet[Quote],
    ) -> list[SymbolIndicator]:

        quotes: DataFrame = DataFrame(list(quotes_for_symbol_and_tu.values()))
        higher_res = quotes[["open", "high", "low", "close"]].max().max()
        lower_supp = quotes[["open", "high", "low", "close"]].min().min()
        prices = self._get_price_counter(quotes)
        if prices:
            best_kmeans = self._find_best_kmeans(prices)
            key_levels = list(best_kmeans.cluster_centers_.flatten())

            key_levels += [higher_res, lower_supp]

            return self._build_symbol_indicator_from_levels(
                symbol=symbol, time_unit=time_unit, key_levels=key_levels
            )
        return []

    def _get_price_counter(self, quotes: DataFrame) -> list[float]:
        counter_level = Counter()
        min_lows, max_lows = self._get_rolling_min_max(quotes, "low")
        counter_level.update(Counter(min_lows))
        counter_level.update(Counter(max_lows))

        min_highs, max_highs = self._get_rolling_min_max(quotes, "high")
        counter_level.update(Counter(min_highs))
        counter_level.update(Counter(max_highs))

        # min_opens, max_opens = self._get_rolling_min_max(quotes, "open")
        # counter_level.update(Counter(min_opens))
        # counter_level.update(Counter(max_opens))
        #
        #
        # min_closes, max_closes = self._get_rolling_min_max(quotes, "close")
        # counter_level.update(Counter(min_closes))
        # counter_level.update(Counter(max_closes))

        counter_level = {
            price: counter for price, counter in counter_level.items() if counter >= 100
        }

        return list(counter_level.keys())

    def _get_rolling_min_max(
        self, quotes_df: DataFrame, column_name: str
    ) -> tuple[Series, Series]:
        rolling_df: Series = quotes_df[column_name].rolling(
            self.window_size, center=self.center, closed=self.closed
        )
        return rolling_df.min().dropna(), rolling_df.max().dropna()

    @staticmethod
    def _find_best_kmeans(prices: list[float]) -> KMeans:
        kmeans_results: dict[float, KMeans] = dict()
        array = np.array(prices).reshape(-1, 1)
        for n_cluster in range(5, int((len(prices) + 1) / 2)):
            kmeans = KMeans(n_clusters=n_cluster)
            kmeans.fit(array)
            labels = kmeans.fit_predict(array)
            silhouette = silhouette_score(array, labels)
            kmeans_results[silhouette] = kmeans
        try:
            return kmeans_results[max(kmeans_results)]
        except:
            breakpoint()

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
