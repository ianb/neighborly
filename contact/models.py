from django.contrib.gis.db import models

class User(models.Model):
    """This represents one user"""
    # The name, as it displays:
    display_name = models.CharField(max_length=100)
    # The user's primary email address (destination address)
    email = models.EmailField()
    # The hash of the user's password:
    password_hash = models.CharField(max_length=40)
    # A free-text listing of the profile information (an About):
    profile_info = models.TextField()
    # The street address (number, street name):
    street_address = models.CharField(max_length=255)
    # city, state, country, zip:
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=10)
    country = models.CharField(max_length=10)
    zip = models.CharField(max_length=10)

    # The geocoded lat/long location of the person:
    location = models.PointField()

    # The radius of things this person wants to listen to:
    listen_radius_miles = models.DecimalField(
        max_digits=5, decimal_places=3)
    # The radius where the person will display their contact info:
    display_in_index_radius_miles = models.DecimalField(
        max_digits=5, decimal_places=3)
    # When the user was created/modified
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    objects = models.GeoManager()

class ExtraEmail(models.Model):
    """These are additional email addresses that should be recognized
    (when getting incoming email)"""
    user = models.ForeignKey(User)
    email = models.EmailField()

class UserService(models.Model):
    """These are links to the user on services like Facebook, etc"""
    user = models.ForeignKey(User)
    service_name = models.CharField(max_length=100)
    url = models.URLField()

class Thread(models.Model):
    """This is the head of a thread (though it does not contain the
    first message)"""
    first_message = models.ForeignKey(
        'Message', related_name='first_message_thread')
    # The first person to send the message
    initiator = models.ForeignKey(User)
    # The subject; it may change, but this subject is what will be
    # displayed on the web:
    subject = models.TextField()
    # The location (probably of the initiator):
    location = models.PointField()
    # Where the initiator said this message was relevant:
    relevance_radius_miles = models.DecimalField(
        max_digits=5, decimal_places=3)

class Message(models.Model):
    """One message, email or via web"""
    # The thread this belongs to;
    thread = models.ForeignKey(Thread)
    # The author of the message:
    author_id = models.ForeignKey(User)
    # The subject field of the message:
    subject = models.TextField()
    # The text/readable body (may strip attachments):
    body = models.TextField()
    # The headers (as raw text):
    headers = models.TextField()
    created = models.DateTimeField()
    # If this was an email, this will be the filename where the complete email is kept:
    raw_email_filename = models.CharField(max_length=255)
