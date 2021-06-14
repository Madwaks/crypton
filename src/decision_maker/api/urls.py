from django.urls import re_path
from rest_framework.schemas import get_schema_view


urlpatterns = [
    re_path(
        r"^$",
        get_schema_view(title="Your Project", description="API for all things …"),
        name="openapi-schema",
    ),
    # path('keyLevels/<str:symbol>', QuoteSymbolView.as_view(), name="Client List"),
]
