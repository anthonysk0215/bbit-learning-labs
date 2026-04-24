import pika
import os
from consumer_interface import mqConsumerInterface

class mqConsumer(mqConsumerInterface):
    def __init__(self, binding_key: str, exchange_name: str, queue_name: str):
        self.binding_key = binding_key
        self.exchange_name = exchange_name
        self.queue_name = queue_name

        self.setupRMQConnection()

    def setupRMQConnection(self):
        '''
        setupRMQConnection Function: Establish connection to the RabbitMQ service, 
        declare a queue and exchange, bind the binding key to the queue on the exchange 
        and finally set up a callback function for receiving messages
        '''
        con_params = pika.URLParameters(os.environ["AMQP_URL"])
        self.connection = pika.BlockingConnection(parameters=con_params)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name)
        self.channel.exchange_declare(exchange=self.exchange_name)
        self.channel.queue_bind(queue=self.queue_name, exchange=self.exchange_name, routing_key=self.binding_key)
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.on_message_callback, auto_ack=False)


    def on_message_callback(self, channel, method_frame, header_frame, body):
        # onMessageCallback: Print the UTF-8 string message and then close the connection.
        print(f"Received Message: {body}")
        

    def startConsuming(self):
        # startConsuming: Consumer should start listening for messages from the queue.
        self.channel.start_consuming()

    def __del__(self):
        # Close the connection and channel
        self.connection.close()
        self.channel.close()
