from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

# celery is a task-delegation tool it has a nifty scheduler called beat


# set the settings to use which is my project settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE",'todoproject.settings')

# create my celery application instance
app=Celery('todoproject')

# specify where the celery app configuration is 
app.config_from_object('django.conf:settings')

# specify where celery application will look for tasks
app.autodiscover_tasks(lambda:settings.INSTALLED_APPS)

# this can also be done in the CELERYBEAT_SCHEDULE attribute in settings module
app.conf.beat_schedule = {
    'send-todo-notification-report-as-per-the-user-time': {
        'task': 'todo.tasks.send_todo_notification_email',
        'schedule': crontab(),  # change to `crontab(minute=0, hour=0)` if you want it to run daily at midnight
        # 'args':(*args) # only add this if your task function takes parameters
    },
}
