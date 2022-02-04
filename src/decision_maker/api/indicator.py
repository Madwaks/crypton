from rest_framework.generics import ListAPIView

from decision_maker.api.serializers.indicator import IndicatorSerializer
from decision_maker.models import Indicator


class IndicatorView(ListAPIView):
    serializer_class = IndicatorSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        symbol = self.kwargs.get("symbol")
        time_unit = self.kwargs.get("time_unit")
        indicator_name = self.kwargs.get("indicator_name")
        return Indicator.objects.filter(
            name=indicator_name, quote__symbol__name=symbol, quote__time_unit=time_unit
        )
