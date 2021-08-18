import json

import pika

# private mqqt key
url_params = open('products/url_parameters.txt').read()
# print(url_params)
params = pika.URLParameters(url_params)

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='admin')


def callback(channel, method, properties, body):
    print('Received in admin')
    _id = json.loads(body)
    print(_id)


channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)

print('started_consuming: admin')

channel.start_consuming()

channel.close()
