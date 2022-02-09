from django.db.models import QuerySet
from injector import singleton
from tqdm import tqdm

from crypto.models import Quote
from decision_maker.models import Distance
from decision_maker.models.enums import AvailableIndicators


@singleton
class DistanceFactory:
    def build_distances(self, quotes: QuerySet[Quote]) -> list[Distance]:
        miss_distances = (
            quotes.prefetch_related("indicators")
            .exclude(indicators=None)
            .filter(distances__isnull=True)
        )
        return [self._build_distance(quote) for quote in miss_distances]

    def _build_distance(self, quote: Quote) -> Distance:
        distance = Distance(quote=quote)
        res, supp = quote.nearest_key_level
        self._set_indicators_to_distance(quote, distance)

        distance.support = (quote.close - supp) / quote.close
        distance.resistance = (quote.close - res) / quote.close
        return distance

    @staticmethod
    def _set_indicators_to_distance(quote: Quote, distance: Distance):
        for indicator_name in AvailableIndicators.values:
            mm = quote.indicators.get(name=indicator_name)
            if mm.value != 0:
                setattr(
                    distance, indicator_name, (quote.close - mm.value) / quote.close
                )
