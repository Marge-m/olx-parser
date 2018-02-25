from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
# from settings import INSTALLED_APPS

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'olx_stats.settings')
# import django
# django.setup()
app = Celery('olx_stats')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
