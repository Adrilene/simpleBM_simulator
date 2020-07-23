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
    block = random.choices([True, False], [1.0, 0.0], k=1)[0]
    SmartTvService().insert_data({'block': block})  # Setar aqui random
    print(SmartTvService().last_record())
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
