from django.views.generic import TemplateView


class CryptoVizView(TemplateView):
    template_name = "crypto_viz.html"
