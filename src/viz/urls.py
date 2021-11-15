from django.conf.urls import url

from viz.views import session_state_view

urlpatterns = [
    url(
        "^demo-eight",
        session_state_view,
        {"template_name": "demo_eight.html"},
        name="demo-eight",
    )
]
