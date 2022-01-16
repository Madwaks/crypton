from django.contrib.admin import ModelAdmin
from django.db.models import QuerySet, F

from crypto.models import Symbol
from decision_maker.models import Distance


class DistanceAdmin(ModelAdmin):
    list_display = (
        "quote",
        "abs_mm7",
        "abs_mm_20",
        "abs_mm_50",
        "abs_mm_100",
        "abs_mm_200",
        "support",
        "resistance",
    )

    def get_queryset(self, request):
        qs = super(DistanceAdmin, self).get_queryset(request).prefetch_related("quote")
        filtered_qs: QuerySet = qs.filter(
            quote__in=[
                symbol.last_quote
                for symbol in Symbol.objects.all().prefetch_related("quotes")
                if symbol.last_quote
            ]
        )
        return filtered_qs

    def abs_mm7(self, obj: Distance):
        return obj.abs_mm7

    def abs_mm_20(self, obj: Distance):
        return obj.abs_mm_20

    def abs_mm_50(self, obj: Distance):
        return obj.abs_mm_50

    def abs_mm_100(self, obj: Distance):
        return obj.abs_mm_100

    def abs_mm_200(self, obj: Distance):
        return obj.abs_mm_200
