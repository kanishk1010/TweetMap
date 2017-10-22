from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^pollution$', views.pollution),
    url(r'^lgbtq$', views.lgbtq),
    url(r'^vegan$', views.vegan),
    url(r'^nk$', views.nk),
    url(r'^modi$', views.modi)
]