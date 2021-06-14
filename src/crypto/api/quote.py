from rest_framework.generics import ListAPIView

from crypto.models import Quote
from crypto.serializers.quote import QuoteSerializer


class QuoteSymbolView(ListAPIView):
    serializer_class = QuoteSerializer

    def get(self, request, *args, **kwargs):
        symbol = kwargs.get("symbol")
        tu = kwargs.get("time_unit", "4h")
        self.queryset = Quote.objects.filter(symbol__name=symbol, time_unit=tu)
        return super(QuoteSymbolView, self).get(request, *args, **kwargs)
