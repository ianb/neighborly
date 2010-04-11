from django.conf.urls.defaults import *
from neighborly.contact import views

urlpatterns = patterns(
    '',
    url(r'^user/(?P<user_id>\d+)?$', views.user),
    url(r'^topic/(?P<topic_id>\d+)$', views.topic),
)
