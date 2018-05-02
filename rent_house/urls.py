from django.conf.urls import include, url
from django.contrib import admin
# from chatterbot.ext.django_chatterbot import urls as chatterbot_urls
from rent_house.views import ChatterBotAppView, ChatterBotView
from rent_house import chatterbot_urls


urlpatterns = [
    url(r'^$', ChatterBotView.as_view(), name='main'),
    url(r'^admin/', admin.site.urls,  name='admin'),
    url(r'^api/chatterbot/', include((chatterbot_urls,'chatterbot_urls'), namespace='chatterbot')),
    # url(r'^api/chatterbot/', ChatterBotAppView.as_view(), name='app')
    # url(r'^api/chatterbot/', include(chatterbot_urls, namespace='chatterbot')),
]
