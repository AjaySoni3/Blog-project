# import os
# from celery import Celery
# from django.conf import settings
# from celery.schedules import crontab
# from datetime import datetime, timedelta
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blogproject.settings')
# app = Celery('blogproject')
# app.conf.enable_utc = False
# app.conf.update(timezone='Asia/Kolkata')
#
# app.config_from_object(settings, namespace='CELERY')
#
# app.conf.beat_schedule = {
# }
# app.autodiscover_tasks()
#
# app.conf.update(
#     BROKER_URL='redis://localhost:6379/0',
# )

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# setting the Django settings module.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blogproject.settings')
app = Celery('blogproject')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Looks up for task modules in Django applications and loads them
app.autodiscover_tasks()


