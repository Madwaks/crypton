from django.contrib.admin import ModelAdmin

from crypto.models import Symbol


class SymbolAdmin(ModelAdmin):
    list_display = (
        "base_asset",
        "quote_asset",
        "last_close",
        "last_mm_7",
        "last_mm_20",
        "last_mm_50",
        "last_mm_100",
        "last_mm_200",
        "next_supp",
        "next_res",
    )

    def last_close(self, obj: Symbol) -> float:
        return obj.last_close

    def last_mm_7(self, obj: Symbol):
        return obj.last_mm_7

    def last_mm_20(self, obj: Symbol):
        return obj.last_mm_20

    def last_mm_50(self, obj: Symbol):
        return obj.last_mm_50

    def last_mm_100(self, obj: Symbol):
        return obj.last_mm_100

    def last_mm_200(self, obj: Symbol):
        return obj.last_mm_200

    def next_supp(self, obj: Symbol):
        return obj.next_supp
