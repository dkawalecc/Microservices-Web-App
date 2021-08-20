import json, pika, os, django

from products.models import Product

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin.settings')
django.setup()

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
    print('Product_id: ' + _id)
    product = Product.objects.get(id=_id)
    product.likes += 1
    product.save()
    print('Product likes increased')


channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)

print('started_consuming: admin')

channel.start_consuming()

channel.close()
