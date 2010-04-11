"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client

class ContactTest(TestCase):
    def test_details(self):
        client = Client()
        response = client.get('/user/3')
        self.failUnlessEqual(response.status_code, 404)

    def test_index(self):
        client = Client()
        response = client.get('/topic/8')
        self.failUnlessEqual(response.status_code, 404)


