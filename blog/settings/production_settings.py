from blog.settings.base import *
import django_heroku


DEBUG = False
django_heroku.settings(locals())

SECURE_SSL_REDIRECT = True
