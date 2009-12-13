from neighborly.contact.models import User, Thread, Message
from django.contrib.gis import admin

admin.site.register(User, admin.OSMGeoAdmin)
admin.site.register(Thread, admin.OSMGeoAdmin)
admin.site.register(Message, admin.OSMGeoAdmin)
