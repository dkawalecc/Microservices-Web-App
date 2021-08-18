import json

import pika

# private mqqt key
from main import Product, db

url_params = open('/app/url_parameters.txt').read()
# print(url_params)
params = pika.URLParameters(url_params)

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='main')


def callback(ch, method, properties, body):
    print('Received in main')
    data = json.loads(body)
    print(data)

    if properties.content_type == 'product_created':
        product = Product(id=data['id'], title=data['title'], image=data['image'])
        db.session.add(product)
        db.session.commit()
        print('Product created')

    elif properties.content_type == 'product_updated':
        product = Product.query.get(data['id'])
        if product is not None:
            product.title = data['title']
            product.image = data['image']
            db.session.commit()
            print('Product updated')

    elif properties.content_type == 'product_deleted':
        product = Product.query.get(data)
        db.session.delete(product)
        db.session.commit()
        print('Product deleted')


channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)

print('started_consuming: main')

channel.start_consuming()

channel.close()
