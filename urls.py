from django.conf.urls.defaults import *

from piston.resource import Resource
from piston.authentication import HttpBasicAuthentication

from neighborly.contact.handlers import UserHandler, TopicHandler

from django.contrib.gis import admin
admin.autodiscover()

user_resource = Resource(handler=UserHandler)
topic_resource = Resource(handler=TopicHandler)

urlpatterns = patterns(
    '',
    url(r'^user/(?P<user_id>\d+)$', user_resource),
    url(r'^topic/(?P<topic_id>\d+)$', topic_resource),

    # Example:
    # (r'^neighborly/', include('neighborly.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    (r'', include('neighborly.contact.urls')),
)
