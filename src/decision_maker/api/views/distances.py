from django.db.models import QuerySet
from rest_framework.generics import ListAPIView

from crypto.models import Symbol
from decision_maker.api.serializers.distances import DistanceSerializer
from decision_maker.models import Distance


class DistanceView(ListAPIView):
    serializer_class = DistanceSerializer
    queryset = Distance.last.all()

    def get_queryset(self):
        queryset = super(DistanceView, self).get_queryset()
        return queryset.filter(quote__time_unit="15m")
