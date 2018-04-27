from django.conf.urls import url
from .views import ChatterBotAppView


urlpatterns = [
    url(
        r'^$',
        ChatterBotAppView.as_view(),
        name='chatterbot',
    ),
]
