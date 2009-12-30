from django.conf.urls.defaults import *
from neighborly.contact import views

urlpatterns = patterns(
    '',
    (r'^login', views.login),
    (r'^$', views.home),
)
