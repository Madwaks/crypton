from django.urls import re_path
from rest_framework.schemas import get_schema_view

from decision_maker.api.indicator import IndicatorView

urlpatterns = [
    re_path(
        r"^$",
        get_schema_view(title="Your Project", description="API for all things …"),
        name="openapi-schema",
    ),
    re_path(
        "mm/(?P<symbol>.+)/(?P<time_unit>.+)/$",
        IndicatorView.as_view(),
        name="Indicators Symbol",
    ),
]
