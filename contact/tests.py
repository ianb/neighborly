"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
import json

class ContactTest(TestCase):
    def test_details(self):
        client = Client()
        response = client.get('/user/3')
        self.failUnlessEqual(response.status_code, 404)
        response = client.post('/user/', json.dumps(dict(
            email="test1@example.com", name="Test Person",
            street="3000 10th Ave S", city="Minneapolis",
            state="MN", postal_code='55407',
            lat_long=[44.948265, -93.260124],
            )),
                               content_type='application/json')
        try:
            data = json.loads(response.content)
        except:
            print 'Response: %r' % response.content
            raise
        self.assertEqual(data.get('email'), 'test1@example.com')
        self.assertEqual(data.get('name'), 'Test Person')
        self.assertEqual(data.get('street'), '3000 10th Ave S')
        url = data['url']
        assert url.startswith('/user/'), 'Odd url: %r' % url
        response = client.get(url)
        data = json.loads(response.content)
        self.assertEqual(data.get('email'), 'test1@example.com')

    def test_index(self):
        client = Client()
        response = client.get('/topic/8')
        self.failUnlessEqual(response.status_code, 404)
