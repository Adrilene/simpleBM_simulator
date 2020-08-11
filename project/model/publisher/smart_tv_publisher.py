import pika
import json
import random
from project.util.construct_scenario import (
    exchange,
    st_info
)
from project.util.config_broker import ConfigScenario
from project.model.service.smart_tv_service import SmartTvService
from threading import Thread


class SmartTvPublisher(ConfigScenario, Thread):
    def __init__(self):
        ConfigScenario.__init__(self)
        Thread.__init__(self)
        self.declare_exchange(exchange, "topic")

    def run(self):
        last = SmartTvService().last_record()
        if not last:
            block = random.choices([True, False], [1.0, 0.0], k=1)[0]
            SmartTvService().insert_data({'block': block})  # Setar aqui random
            last = SmartTvService().last_record()

        last = last["block"]
        message = {"type": "status", "block": last}
        self.channel.basic_publish(
            exchange=exchange,
            routing_key=st_info,
            properties=pika.BasicProperties(delivery_mode=2,),
            body=json.dumps(message),
        )
        print("(Publish) ", message)
