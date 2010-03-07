import re

from piston.handler import BaseHandler
from piston.utils import rc, throttle

from neighborly.contact.models import User, Topic
from django.contrib.gis.geos import Point
from django.http import HttpResponse
from django.http import HttpResponseNotFound

class UserHandler(BaseHandler):
    allowed_methods = ('GET', 'PUT', 'DELETE')
    fields = ('email', 'name', 'address', 'lat_long', 'profile_info')
    exclude = ('id', re.compile(r'^private_'), 'password_hash')
    model = User

    @classmethod
    def lat_long(cls, user):
        loc = user.location
        return [loc.lat, loc.long]

    def read(self, request, user_id):
        try:
            user = User.objects.get(id=int(user_id))
        except User.DoesNotExist:
            return HttpResponseNotFound()
        return user

    def update(self, request, user_id):
        user = User.objects.get(user_id=int(user_id))
        data = request.PUT
        for field in ['email', 'name', 'address', 'profile_info']:
            if field in data:
                setattr(user, field, data['email'])
        if 'lat_long' in data:
            user.location = Point(data['lat_long'][0], data['lat_long'][1])
        user.save()
        return user

    def delete(self, request, user_id):
        user = User.objects.get(user_id=int(user_id))
        # check that authenticated user is admin
        user.delete()
        return rc.DELETED

class TopicHandler(BaseHandler):
    allowed_methods = ('GET', 'PUT', 'DELETE')
    fields = ('url', 'center', 'subject', 'author', 'last_updated', 'messages') # author=Topic.initiator
    exclude = ('id', 'first_message', '')
    model = Topic

    def read(self, request, topic_id):
        try:
            topic = Topic.objects.get(id=int(topic_id))
        except Topic.DoesNotExist:
            return HttpResponseNotFound()
        return topic

    def update(self, request, topic_id):
        topic = Topic.objects.get(topic_id=int(topic_id))
        #...
        return topic

    def delete(self, request, topic_id):
        topic = Topic.objects.get(topic_id=int(topic_id))
        # check that authenticated user is topic initiator or admin
        topic.delete()
        return rc.DELETED

