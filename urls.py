from django.conf.urls.defaults import *

from django.contrib.gis import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    # Admin screens:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),

    # Main application:
    (r'', include('neighborly.contact.urls')),
)
