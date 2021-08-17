import pika

# private mqqt key
url_params = open('/app/products/url_parameters.txt').read()
# print(url_params)
params = pika.URLParameters(url_params)

connection = pika.BlockingConnection(params)

channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='admin', body='hello main', properties=properties)
