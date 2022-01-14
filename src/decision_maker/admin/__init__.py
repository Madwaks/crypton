from django.contrib import admin

from decision_maker.admin.models.distance import DistanceAdmin
from decision_maker.admin.models.indicator import IndicatorAdmin
from decision_maker.models import Indicator
from decision_maker.models.distance import Distance

admin.site.register(Indicator, IndicatorAdmin)
admin.site.register(Distance, DistanceAdmin)
