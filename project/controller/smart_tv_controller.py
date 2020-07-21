from project.model.subscriber.smart_tv_subscriber import SmartTvSubscriber
from project.model.service.smart_tv_service import SmartTvService
from time import sleep
import random
from datetime import datetime

sp_on = False


def tv_connect():
    global tv_on
    tv_on = True
    subscriber = SmartTvSubscriber()
    random.seed(datetime.now())
    # block = random.choices([True, False], [0.90, 0.10], k=1)[0]
    SmartTvService().insert_data(dict(block=False))  # Setar aqui random
    subscriber.start()
    while True:
        sleep(1)
        if not tv_on:
            subscriber.stop()
            break


def tv_disconnect():
    global tv_on
    tv_on = False


def block_tv(blocked):
    if blocked:
        SmartTvService().insert_data(dict(block=True))
    else:
        SmartTvService().insert_data(dict(block=False))
