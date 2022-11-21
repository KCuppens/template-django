from __future__ import absolute_import

import os

from django.conf import settings

from celery import Celery
from kombu.entity import Exchange, Queue


# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{app_name}.settings.production")
app = Celery("{app_name}")  # , broker=settings.CELERY_BROKER_URL)
app.conf.ONCE = settings.CELERY_ONCE  # force CELERY_ONCE to load settings

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")
# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


# Using a string here means the worker will not have to
# pickle the object when using Windows.
# app.config_from_object('django.conf:settings')
# app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])
# app.conf.ONCE = {
#    'backend': 'celery_once.backends.Redis',
#    'settings': {
#        'url': settings.CELERY_BROKER_URL,
#        'default_timeout': 60 * 5
#    }
# }
app.conf.task_default_queue = "default"
app.conf.task_queues = (
    Queue(
        settings.APP_CONFIG + "default",
        Exchange("normal"),
        routing_key=settings.APP_CONFIG + "default",
        queue_arguments={"x-max-priority": 7},
    ),
    Queue(
        settings.APP_CONFIG + "mailing",
        Exchange("high"),
        routing_key=settings.APP_CONFIG + "mailing",
        queue_arguments={"x-max-priority": 10},
    ),
)
CELERY_DEFAULT_QUEUE = "normal"
CELERY_DEFAULT_EXCHANGE = "normal"
CELERY_DEFAULT_ROUTING_KEY = settings.APP_CONFIG + "default"


class CeleryOnceFakeBackend:
    def __init__(self, settings):
        pass

    def raise_or_lock(self, key, timeout):
        return

    def clear_lock(self, key):
        return
