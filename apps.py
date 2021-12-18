import time
import datetime
import threading
import json
from random import random, uniform

from django.apps import AppConfig
from django_eventstream import send_event

# This is the ASGI entry point and will get loaded automatically when INSTALLED_APPS contains Stockpusher (the
# 'name' field in the class).
class StockpusherConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'StockPusher'

    # This is executed as soon as the app registry is fully populated.
    def ready(self):
        ensure_worker_started()


worker_started = False


def ensure_worker_started():
    global worker_started

    if worker_started:
        return

    if not is_db_ready():
        return

    worker_started = True

    thread = threading.Thread(target=send_worker)
    thread.daemon = True
    thread.start()


def send_worker():
    stocks = {
        "AAPL": 95.0,
        "MSFT": 50.0,
        "AMZN": 300.0,
        "GOOG": 550.0,
        "YHOO": 35.0,
        # "FB": 75.0
    }

    while True:
        # data = datetime.datetime.utcnow().isoformat()

        for key in stocks:
            rando = uniform(-1.0, 1.0)
            # print("Rando: " + rando)
            stocks[key] += rando
        send_event('time', 'message', stocks)
        time.sleep(2)


def is_db_ready():
    from django.db import DatabaseError
    from django_eventstream.models import Event
    try:
        # see if db tables are present
        Event.objects.count()
        return True
    except DatabaseError:
        return False