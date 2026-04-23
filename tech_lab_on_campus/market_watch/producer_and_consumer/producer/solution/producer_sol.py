import pika
import os

from producer_interface import mqProducerInterface

class mqProducer(mqProducerInterface):
    def __init__(self, routing_key: str, exchange_name: str) -> None:
        self.routing_key = routing_key
        self.exchange_name = exchange_name
        self.setupRMQConnection()

    def setupRMQConnection(self) -> None:
        """
        setupRMQConnection Function: Establish connection to the RabbitMQ service.
        """
        con_params = pika.URLParameters(os.environ["AMQP_URL"])
        self.connection = pika.BlockingConnection(parameters=con_params)
        self.channel = self.connection.channel()
        # Create the exchange if not already present
        self.exchange = self.channel.exchange_declare(exchange=self.exchange_name)


    def publishOrder(self, message: str) -> None:
        """
        publishOrder: Publish a simple UTF-8 string message from the parameter.
        publishOrder: Close Channel and Connection.
        """
        self.channel.basic_publish(
            exchange=self.exchange_name,
            routing_key=self.routing_key,
            body=message,
        )

        self.channel.close()
        self.connection.close()

