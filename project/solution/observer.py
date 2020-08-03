import pika
import threading
import json
from time import sleep
from pyrabbit.api import Client


class Observer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="localhost")
        )
        self.queue = "observer"
        self.channel = self.connection.channel()
        self.channel.queue_declare(self.queue)
        self.adaptation = False
        self.steps_to_adapt = None
        self.steps_for_normal_behave = None
        self.messages_types = None
        self.exceptional_scenarios = None
        self.subscribe_in_all_queues()

    def run(self):
        print(
            " [*] Observer is waiting for messages."
            + " To exit press CTRL+C"
        )
        self.channel.basic_consume(
            queue=self.queue, on_message_callback=self.callback,
            auto_ack=False
        )
        self.channel.start_consuming()

    def get_bindings(self):
        client = Client("localhost:15672", "guest", "guest")
        bindings = client.get_bindings()
        bindings_result = []

        for b in bindings:
            if b["source"] == "exchange_baby_monitor":
                bindings_result.append(b)

        return bindings_result

    def subscribe_in_all_queues(self):
        bindings = self.get_bindings()

        for bind in bindings:
            self.channel.queue_bind(
                exchange=bind["source"],
                queue=self.queue,
                routing_key=bind["routing_key"],
            )
            print("Subscribed in ", bind["routing_key"])
        return bindings

    def callback(self, ch, method, properties, body):
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print(
            " [OBSERVER] Receive: %r Data: %r" % (method.routing_key, body)
        )
        body = json.loads(body.decode("UTF-8"))
        if body['type'] in self.messages_types:
            self.read_message(body, method.routing_key)

    def define_messages(self, types: list):
        self.messages_types = types

    def stop(self):
        raise SystemExit()

    def read_message(self, message, source):
        if message["type"] == "notification":
            print("ACTION - I've received a notification message.")
            if self.adaptation:
                print("ACTION - My adaptation failed.")

        if message["type"] == "confirmation":
            if self.adaptation:
                print("ACTION - My adaptation succeeded.")
                self.adaptation = False
                self.return_normal_behave()

        if (
            message["type"] == "status" and
            source == "st_info" and
            message["block"]
        ):
            print("ACTION - I'm going to unlock the TV.")
            self.adaptation = True
            self.adaptation_action()

    def adaptation_action(self):
        for function, params in self.steps_to_adapt:
            function(*params)
        sleep(1)

    def return_normal_behave(self):
        print("ACTION - I'm going to lock the TV.")
        for function, params in self.steps_for_normal_behave:
            function(*params)
