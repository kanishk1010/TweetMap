from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^(?P<keyword>[a-z]+)/(?P<size>[0-9]+)/(?P<geocode>[01])/(?P<random>[01])$', views.search)
]