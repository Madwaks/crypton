from django.urls import path

from viz.plotly_apps import app
from viz.views.crypto_viz import CryptoVizView

urlpatterns = [path("", CryptoVizView.as_view(), name="crypto")]
