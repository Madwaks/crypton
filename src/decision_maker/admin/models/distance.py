from django.contrib.admin import ModelAdmin
from django.db.models import QuerySet, F

from crypto.models import Symbol


class DistanceAdmin(ModelAdmin):
    list_display = (
        "quote",
        "MM7",
        "MM20",
        "MM50",
        "MM100",
        "MM200",
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

    def get_ordering(self, request):
        pass

    # def get_queryset(self, request):
    #     qs = super(ShotsAdmin, self).get_queryset(request)
    #     qs = qs.annotate(ratio=F('hits') * 100 / F('all'))
    #     return qs

    def get_abs_mm7(self, obj):
        return obj.abs_mm7

    get_abs_mm7.admin_order_field = "abs_mm7"
