import pika

params = pika.URLParameters('amqps://jxguwpom:CKYuMeBMrcOF8Ba0UDNakdErtMtRxUA9@rattlesnake.rmq.cloudamqp.com/jxguwpom')

connection = pika.BlockingConnection(params)

channel = connection.channel()


def publish(method, body):
    channel.basic_publish(exchange='', routing_key='admin', body='hello')
