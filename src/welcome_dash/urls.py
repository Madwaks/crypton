from django.urls import path

from welcome_dash.views.home import Home

# Load the dash app to render in template
from welcome_dash.app import financial  # noqa: F401


urlpatterns = [path("", Home.as_view(), name="home")]
