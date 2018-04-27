from django.conf.urls import include, url
from django.contrib import admin
from chatterbot.ext.django_chatterbot import urls as chatterbot_urls
from rent_house.views import ChatterBotAppView


urlpatterns = [
    url(r'^$', ChatterBotAppView.as_view(), name='main'),
    url(r'^admin/', admin.site.urls,  name='admin'),
    url(r'^api/chatterbot/', include((chatterbot_urls,'chatterbot_urls'), namespace='chatterbot')),
]
