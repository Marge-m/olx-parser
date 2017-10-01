from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from olx_stats import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'olx_stats.settings')
app = Celery('olx')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
