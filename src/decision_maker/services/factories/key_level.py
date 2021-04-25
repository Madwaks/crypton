from collections import Counter

import numpy as np
from injector import singleton
from pandas import DataFrame, Series
from sklearn.cluster import KMeans

from core.models import Company


@singleton
class KeyLevelFactory:
    window_size: int = 50
    nb_digits: int = 2
    center: bool = False

    def build_key_level_for_company(self, company: Company) -> list[float]:

        quotes: DataFrame = company.quotes.get_as_dataframe()
        kmeans = KMeans(n_clusters=self._compute_nb_clusters(quotes))

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
        prices = list(counter_level.keys())

        kmeans.fit(np.array(prices).reshape(-1, 1))

        key_levels = list(kmeans.cluster_centers_.flatten())
        return sorted(key_levels)

    def _get_rolling_min_max(
        self, quotes_df: DataFrame, column_name: str
    ) -> tuple[Series, Series]:
        rolling_df: Series = quotes_df[column_name].rolling(
            self.window_size, center=self.center
        )
        return rolling_df.min().dropna(), rolling_df.max().dropna()

    @staticmethod
    def _compute_nb_clusters(quotes_df: DataFrame) -> int:
        return 15
