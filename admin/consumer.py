import pika

# private mqqt key
url_params = open('products/url_parameters.txt').read()
# print(url_params)
params = pika.URLParameters(url_params)

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='main')


def callback(channel, method, properties, body):
    print('Received in admin')
    print(body.decode('utf-8'))


channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)

print('started_consuming')

channel.start_consuming()

channel.close()
