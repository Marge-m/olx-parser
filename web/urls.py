from django.conf.urls import url

from web.views import web_hook

urlpatterns = [
    url(r'^$', web_hook),
]
