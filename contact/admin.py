from neighborly.contact.models import User, Topic, Message
from django.contrib.gis import admin

admin.site.register(User, admin.OSMGeoAdmin)
admin.site.register(Topic, admin.OSMGeoAdmin)
admin.site.register(Message, admin.OSMGeoAdmin)
