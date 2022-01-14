from django.contrib.admin import ModelAdmin


class QuoteAdmin(ModelAdmin):
    search_fields = ("symbol__name",)
    ordering = ("-timestamp",)
