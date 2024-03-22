from __future__ import absolute_import, unicode_literals

import os
from celery import Celery
from celery.schedules import crontab
from celery.schedules import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

app = Celery('mysite')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# app.conf.beat_schedule = {
#     'create-daily-data': {
#         'task': 'app.tasks.calculate_daily_revenue',  
#         'schedule': timedelta(seconds=5),
#     },
# }