from django.contrib.admin import ModelAdmin
from django.db.models import QuerySet, F

from crypto.models import Quote, Symbol


class DistanceAdmin(ModelAdmin):
    list_display = (
        "quote",
        "abs_mm7",
        "mm20",
        "mm50",
        "mm100",
        "mm200",
        "support",
        "resistance",
    )

    def get_queryset(self, request):
        qs = super(DistanceAdmin, self).get_queryset(request)
        filtered_qs: QuerySet = qs.filter(
            quote__in=[
                symbol.last_quote
                for symbol in Symbol.objects.all().prefetch_related("quotes")
                if symbol.last_quote
            ]
        )
        annotated_qs = filtered_qs.annotate(abs_mm7=abs(F("mm7")))

    def get_ordering(self, request):
        pass

    # def get_queryset(self, request):
    #     qs = super(ShotsAdmin, self).get_queryset(request)
    #     qs = qs.annotate(ratio=F('hits') * 100 / F('all'))
    #     return qs

    def get_ratio(self, obj):
        return obj.abs_mm7

    get_ratio.admin_order_field = "abs_mm7"
