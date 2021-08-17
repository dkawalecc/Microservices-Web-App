import pika

# private mqqt key
url_params = open('url_parameters.txt').read()
params = pika.URLParameters(url_params)

connection = pika.BlockingConnection(params)

channel = connection.channel()


def publish(method, body):
    channel.basic_publish(exchange='', routing_key='admin', body='hello')
