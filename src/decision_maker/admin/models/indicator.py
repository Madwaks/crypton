from django.contrib.admin import ModelAdmin


class IndicatorAdmin(ModelAdmin):
    list_display = ('name','value','quote', )
