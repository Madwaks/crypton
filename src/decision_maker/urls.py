from django.urls import path

from decision_maker.views.key_level import KeyLevelView
from decision_maker.views.screener import ScreenerCreate, ScreenerTest

urlpatterns = [
    path("", ScreenerCreate.as_view()),
    path("test", ScreenerTest.as_view()),
    path("key-level", KeyLevelView.as_view()),
]
