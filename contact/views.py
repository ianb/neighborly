# Create your views here.
import json
from django.http import HttpResponse
from neighborly.contact.models import User, Topic
from django.shortcuts import get_object_or_404
from django.contrib.gis.geos import Point

def json_response(data):
    data = json.dumps(data)
    return HttpResponse(data, content_type='application/json')

def date_to_string(date):
    return date.strftime('%Y-%d-%mT%H:%M:%S')


def home(req):
    return HttpResponse('homepage')

def login(req):
    return HttpResponse('login')

def user(req, user_id=None):
    if user_id is None and req.method == 'POST':
        return user_create(req)
    user = get_object_or_404(User, pk=int(user_id))
    if req.method == 'GET':
        return user_read(req, user)
    elif req.method == 'PUT':
        return user_update(req, user)
    else:
        assert 0

def user_create(req):
    data = json.loads(req.raw_post_data)
    try:
        location = Point(data['lat_long'])
    except:
        import sys
        print >> sys.stderr, 'Bad lat_long: %r' % data['lat_long']
        raise
    user = User(
        email=data['email'],
        name=data['name'],
        street=data['street'],
        city=data['city'],
        state=data['state'],
        postal_code=data['postal_code'],
        location=location,
        profile_info=data.get('profile_info', ''),
        )
    user.save()
    return user_read(req, user)

def user_read(req, user):
    return json_response(dict(
        url=user.resource_url,
        name=user.name,
        email=user.email,
        profile_info=user.profile_info,
        street=user.street,
        city=user.city,
        state=user.state,
        postal_code=user.postal_code,
        lat_long=[user.location.x, user.location.y],
        listen_radius_members=user.listen_radius_members,
        display_in_index_members=user.display_in_index_members,
        created=date_to_string(user.created),
        modified=date_to_string(user.modified),
        ))

def user_update(req, user):
    data = json.loads(req.raw_post_data)
    for field in ['email', 'name', 'profile_info', 'street', 'city', 'state', 'postal_code',
                  'listen_radius_members', 'display_in_index_members']:
        if field in data:
            setattr(user, field, data[field])
    if 'lat_long' in data:
        user.location = Point(data['lat_long'])
    user.save()
    return user_read(user)

def topic(req, topic_id=None):
    if topic_id is None and req.method == 'POST':
        return topic_create(req)
    topic = get_object_or_404(Topic, pk=int(topic_id))
    if req.method == 'GET':
        return topic_read(req, topic)
    elif req.method == 'PUT':
        return topic_update(req, topic)
    else:
        assert 0
