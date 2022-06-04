from django.db.models import QuerySet
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView

from crypto.models import Symbol
from crypto.utils.etc import SYMBOLS_TO_COMPUTE
from decision_maker.api.serializers.distances import DistanceSerializer
from decision_maker.models import Distance
from decision_maker.utils.indicators.compute_indicators import IndicatorComputer
from utils.enums import TimeUnits
from utils.service_provider import provide


class DistanceView(ListAPIView):
    serializer_class = DistanceSerializer
    queryset = Distance.last.all()

    def get_queryset(self):
        queryset = super(DistanceView, self).get_queryset()
        time_unit = TimeUnits.from_code(self.request.GET.get("time_unit"))
        if time_unit is None:
            raise NotFound(f"Wrong query params :{self.request.GET.get('time_unit')}")
        symbols = self._select_symbols(SYMBOLS_TO_COMPUTE, time_unit=time_unit)
        distances = queryset.filter(quote__time_unit=time_unit).prefetch_related(
            "quote__symbol"
        )
        if distances:
            symbols_in_distances = distances.distinct("quote__symbol").values_list(
                "quote__symbol", flat=True
            )
            symbols_to_import = symbols.exclude(pk__in=symbols_in_distances)
            if symbols_to_import:
                self._compute_missing_last_distances(
                    symbols_to_import, time_unit=time_unit
                )
        else:
            self._compute_missing_last_distances(symbols, time_unit=time_unit)
        distances = queryset.filter(quote__time_unit=time_unit).prefetch_related(
            "quote__symbol"
        )

        return distances

    def _compute_missing_last_distances(
        self, symbols: list[Symbol], time_unit: TimeUnits
    ):
        ind_computer = provide(IndicatorComputer)
        for symbol in symbols:
            ind_computer.compute_indicators_for_symbol(symbol, time_unit)

    def _select_symbols(self, symbols: QuerySet, time_unit: TimeUnits):
        symbols_to_keep = [
            symb.pk
            for symb in symbols
            if symb.quotes.get_mean_volume(500, time_unit)
            * symb.quotes.get_mean_price(500, time_unit)
            > 200_000
        ]
        return symbols.filter(pk__in=symbols_to_keep)
