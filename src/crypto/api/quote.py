from rest_framework.generics import ListAPIView

from crypto.models import Quote
from crypto.serializers.quote import QuoteSerializer


class QuoteSymbolView(ListAPIView):
    serializer_class = QuoteSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        symbol = self.kwargs.get("symbol")
        time_unit = self.kwargs.get("time_unit")
        return Quote.objects.filter(symbol__name=symbol, time_unit=time_unit)
