import sys
from dataclasses import dataclass
from flask import Flask, jsonify, abort
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
import requests

from producer import publish

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@db/main'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)

db = SQLAlchemy(app)


@dataclass
class Product(db.Model):
    id: int
    title: str
    image: str

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(200))
    image = db.Column(db.String(200))


@dataclass()
class ProductUser(db.Model):
    id: int
    user_id: int
    product_id: int

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)

    UniqueConstraint('user_id', 'product_id', name='user_product_unique')


@app.route('/api/products')
def index():
    return jsonify(Product.query.all())


@app.route('/api/products/<int:id>')
def item(id):
    return jsonify(Product.query.get(id))


@app.route('/api/products/<int:id>/like', methods=['POST'])
def like(id):
    try:
        req = requests.get('http://docker.for.win.localhost:8000/api/user', timeout=0.1)
        json = req.json()

        try:
            product_user = ProductUser(user_id=json['id'], product_id=id)
            db.session.add(product_user)
            db.session.commit()

            publish('product_liked', id)
        except SystemError:
            abort(400, 'You already liked this product')

        return jsonify({
            'message': 'success'
        })
    except requests.exceptions.RequestException as e:
        print(e)
        return "No response"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
