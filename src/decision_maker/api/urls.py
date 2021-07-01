from django.urls import re_path
from rest_framework.schemas import get_schema_view

from decision_maker.api.indicator import IndicatorView
from decision_maker.api.key_level import KeyLevelView

urlpatterns = [
    re_path(
        r"^$",
        get_schema_view(title="Your Project", description="API for all things …"),
        name="openapi-schema",
    ),
    re_path(
        "(?P<indicator_name>.+)/(?P<symbol>.+)/(?P<time_unit>.+)/$",
        IndicatorView.as_view(),
        name="Indicators Symbol",
    ),
    re_path(
        "key_level/(?P<symbol>.+)/(?P<time_unit>.+)/$",
        KeyLevelView.as_view(),
        name="KeyLevel Symbol",
    ),
]
