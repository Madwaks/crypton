from django.urls import re_path
from rest_framework.schemas import get_schema_view

from crypto.api.quote import QuoteSymbolView


urlpatterns = [
    re_path(
        r"^$",
        get_schema_view(title="Your Project", description="API for all things …"),
        name="openapi-schema",
    ),
    re_path(
        "quotes/(?P<symbol>.+)/(?P<time_unit>.+)/",
        QuoteSymbolView.as_view(),
        name="Symbol quotes",
    ),
]
