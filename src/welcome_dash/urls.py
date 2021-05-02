from django.urls import path

from welcome_dash.views.home import Home

urlpatterns = [path("", Home.as_view(), name="home")]
