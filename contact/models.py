from django.contrib.gis.db import models

class User(models.Model):
    display_name = models.CharField(max_length=100)
    email = models.EmailField()
    password_hash = models.CharField(max_length=40)
    contact_info = models.TextField()
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=10)
    country = models.CharField(max_length=10)
    zip = models.CharField(max_length=10)
    
    location = models.PointField()

    listen_radius_miles = models.DecimalField(
        max_digits=5, decimal_places=3)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    objects = models.GeoManager()

class Thread(models.Model):
    first_message = models.ForeignKey(
        'Message', related_name='first_message_thread')
    subject = models.TextField()
    location = models.PointField()
    relevance_radius_miles = models.DecimalField(
        max_digits=5, decimal_places=3)

class Message(models.Model):
    thread = models.ForeignKey(Thread)
    author_id = models.ForeignKey(User)
    subject = models.TextField()
    body = models.TextField()
    headers = models.TextField()
    created = models.DateTimeField()
    raw_email_filename = models.CharField(max_length=255)
