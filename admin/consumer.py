import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin.settings')

import json, pika, django
# from django.conf import settings

# settings.configure(default_settings="admin.settings", DEBUG=True)
django.setup()
from products.models import Product

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
    print(f'Product_id: {_id}')
    product = Product.objects.get(id=_id)
    product.likes += 1
    product.save()
    print('Product likes increased')


channel.basic_consume(
    queue='admin', on_message_callback=callback, auto_ack=True)

print('started_consuming: admin')

channel.start_consuming()

channel.close()
