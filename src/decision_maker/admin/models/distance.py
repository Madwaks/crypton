from django.contrib.admin import ModelAdmin


class DistanceAdmin(ModelAdmin):
    list_display = ("mm7", "mm20", "mm50", "mm100", "mm200", "support", "resistance")
