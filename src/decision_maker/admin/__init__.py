from django.contrib import admin

from decision_maker.admin.models.indicator import IndicatorAdmin
from decision_maker.models import Indicator

admin.site.register(Indicator, IndicatorAdmin)
