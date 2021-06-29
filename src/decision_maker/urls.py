from django.urls import path, include


urlpatterns = [path("api/", include("decision_maker.api.urls"))]
