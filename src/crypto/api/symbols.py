from rest_framework.generics import ListAPIView

from crypto.models import Symbol, Quote
from crypto.serializers.symbol import SymbolSerializer


class SymbolView(ListAPIView):
    serializer_class = SymbolSerializer

    def get_queryset(self):
        available_symbols = Quote.objects.order_by().values("symbol").distinct()
        return Symbol.objects.filter(pk__in=available_symbols)
