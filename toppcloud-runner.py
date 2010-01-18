# Note: the virtualenv path has already been setup at this time

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
