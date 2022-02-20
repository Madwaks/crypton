from django.db.models import QuerySet
from rest_framework.generics import ListAPIView

from crypto.models import Symbol
from decision_maker.api.serializers.distances import DistanceSerializer
from decision_maker.models import Distance


class DistanceView(ListAPIView):
    serializer_class = DistanceSerializer

    def get_queryset(self):
        available_symbols = Symbol.objects.exclude(quotes=None).prefetch_related(
            "last_quote"
        )
        filtered_qs: QuerySet = Distance.objects.filter(
            quote__in=[
                symbol.get_last_quote
                for symbol in available_symbols
                if symbol.get_last_quote
            ]
        )
        return filtered_qs
