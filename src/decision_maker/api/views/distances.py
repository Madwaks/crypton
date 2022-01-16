from django.db.models import QuerySet
from rest_framework.generics import ListAPIView

from crypto.models import Symbol
from decision_maker.api.serializers.distances import DistanceSerializer
from decision_maker.models import Distance


class DistanceView(ListAPIView):
    serializer_class = DistanceSerializer

    def get_queryset(self):
        filtered_qs: QuerySet = Distance.objects.filter(
            quote__in=[
                symbol.last_quote
                for symbol in Symbol.objects.exclude(quotes=None).prefetch_related(
                    "quotes"
                )
                if symbol.last_quote
            ]
        )
        return filtered_qs
