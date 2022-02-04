from rest_framework.generics import ListAPIView

from decision_maker.api.serializers.indicator import SymbolIndicatorSerializer
from decision_maker.models import SymbolIndicator


class KeyLevelView(ListAPIView):
    serializer_class = SymbolIndicatorSerializer

    def get_queryset(self):
        symbol = self.kwargs.get("symbol")
        time_unit = self.kwargs.get("time_unit")
        return SymbolIndicator.objects.filter(symbol__name=symbol, time_unit=time_unit)
