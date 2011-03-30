import os
import sys
sys.path.append('/srv/django2/wall')
sys.path.append('/srv/django2')
os.environ['DJANGO_SETTINGS_MODULE'] = 'wall.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
