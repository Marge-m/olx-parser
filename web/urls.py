from django.conf.urls import url

from web.views import HomeView, RequestCrawlingView

urlpatterns = [
    url(r'^$', HomeView.as_view()),
    url(r'^charts/(?P<pk>[-\w]+)$', RequestCrawlingView.as_view(), name='charts')
]
