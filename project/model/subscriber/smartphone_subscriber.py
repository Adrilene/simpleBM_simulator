import threading
import json
from project.util.config_broker import ConfigScenario
from project.util.construct_scenario import (
    exchange,
    queue_smartphone_bm,
    queue_smartphone_st,
    bm_info,
    st_info,
)
from project.model.publisher.smartphone_publisher import SmartphonePublisher
from threading import Thread
from project.model.business.smartphone_business import (
    check_user_confirm,
    check_is_notification,
    forward_message_smart_tv
)
from time import sleep

data = None
count_attempts = 0


class SmartphoneSubscriber(ConfigScenario, Thread):
    def __init__(self, type_consume):
        ConfigScenario.__init__(self)
        Thread.__init__(self)
        self.channel.queue_delete(queue=queue_smartphone_bm)
        self.channel.queue_delete(queue=queue_smartphone_st)
        self._stop = threading.Event()
        self.type_consume = type_consume
        self.declare_exchange(exchange, "topic")
        self.declare_queue(queue_smartphone_bm)
        self.declare_queue(queue_smartphone_st)

    def run(self):
        if self.type_consume == "babymonitor":
            self.bind_exchange_queue(exchange, queue_smartphone_bm, bm_info)
            self.consume_message_baby_monitor()
        if self.type_consume == "smart_tv":
            self.bind_exchange_queue(exchange, queue_smartphone_st, st_info)
            self.consume_message_tv()

    def stop(self):
        if self.type_consume == "babymonitor":
            print("(Subscribe) SP|BM: Close")
            # self.channel.queue_delete(queue=queue_smartphone_bm)
            self._stop.set()
            self._stop.isSet()
        else:
            print("(Subscribe) SP|TV: Close")
            # self.channel.queue_delete(queue=queue_smartphone_st)
            self._stop.set()
            self._stop.isSet()

    def consume_message_baby_monitor(self):
        print(
            " [*] Smartphone waiting for messages from Baby Monitor."
            + " To exit press CTRL+C"
        )
        self.channel.basic_consume(
            queue=queue_smartphone_bm,
            on_message_callback=self.callback_babymonitor_sm,
            auto_ack=False,
        )

        self.channel.start_consuming()

    def consume_message_tv(self):
        print(
            " [*] Smartphone waiting for messages from TV." +
            " To exit press CTRL+C"
        )

        self.channel.basic_consume(
            queue=queue_smartphone_st,
            on_message_callback=self.callback_smart_tv,
            auto_ack=False,
        )

        self.channel.start_consuming()

    def callback_babymonitor_sm(self, ch, method, properties, body):
        ch.basic_ack(delivery_tag=method.delivery_tag)
        body = body.decode("UTF-8")
        body = json.loads(body)
        print('FROM BABYMONITOR: ', body)
        notification = check_is_notification(body)
        if notification:
            if body["time_no_breathing"] == 10:
                forward_message_smart_tv()

    def callback_smart_tv(self, ch, method, properties, body):
        global count_attempts

        ch.basic_ack(delivery_tag=method.delivery_tag)
        body = body.decode("UTF-8")
        body = json.loads(body)
        print('FROM SMARTTV: ', body)
        sleep(1)
        confirm = check_user_confirm()
        if body["block"] and not confirm:
            # forward again
            if count_attempts >= 3:
                send_confirm = input(
                    'Many attempts to forward.' +
                    'Do you want to send confirmation? [s/n]'
                )
                if send_confirm == 's':
                    SmartphonePublisher("confirmation").start()
                    return
            forward_message_smart_tv()
            count_attempts += 1
        else:
            # send confirmation to BM
            SmartphonePublisher("confirmation").start()
