from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from data import users, orders, offers
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///memory:"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JSON_AS_ASCII"] = False

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    role = db.Column(db.String(100))
    phone = db.Column(db.String(100))


class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(255))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    address = db.Column(db.String(100))
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Offer(db.Model):
    __tablename__ = "offer"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))


def get_users_offers_orders():
    new_users = []
    for user in users:
        new_users.append(
            User(
                id=user['id'],
                first_name=user['first_name'],
                last_name=user['last_name'],
                age=user['age'],
                email=user['email'],
                role=user['role'],
                phone=user['phone'],
            )
        )
        with db.session.begin():
            db.session.add_all(new_users)

    new_offers = []
    for offer in offers:
        new_offers.append(
            Offer(
                id=offer['id'],
                order_id=offer['order_id'],
                executor_id=offer['executor_id'],
            )
        )
        with db.session.begin():
            db.session.add_all(new_offers)

    new_orders = []
    for order in orders:
        new_orders.append(
            Order(
                id=order['id'],
                name=order['name'],
                description=order['description'],
                start_date=datetime.strptime(order['start_date'], '%m/%d/%Y'),
                end_date=datetime.strptime(order['end_date'], '%m/%d/%Y'),
                address=order['address'],
                price=order['price'],
                customer_id=order['customer_id'],
                executor_id=order['executor_id'],
            )
        )
        with db.session.begin():
            db.session.add_all(new_orders)


@app.route('/orders', methods=['GET', 'POST'])
def orders_index():
    if request.method == 'GET':
        show_orders = []
        for order in Order.query.all():
            show_orders.append({
                "id": order.id,
                "name": order.name,
                "description": order.description,
                "start_date": order.start_date,
                "end_date": order.end_date,
                "address": order.address,
                "price": order.price,
                "customer_id": order.customer_id,
                "executor_id": order.executor_id,
            })
        return jsonify(show_orders)

    elif request.method == 'POST':
        data = request.get_json()
        new_order = Order(
            id=data['id'],
            name=data['name'],
            description=data['description'],
            start_date=datetime.strptime(data['start_date'], '%m/%d/%Y'),
            end_date=datetime.strptime(data['end_date'], '%m/%d/%Y'),
            address=data['address'],
            price=data['price'],
            customer_id=data['customer_id'],
            executor_id=data['executor_id'],
        )
        with db.session.begin():
            db.session.add(new_order)
    return '', 200


@app.route('/orders/<int:id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def id_orders_index(id):
    if request.method == 'GET':
        order_id = Order.query.get(id)
        return jsonify({
            "id": order_id.id,
            "name": order_id.name,
            "description": order_id.description,
            "start_date": order_id.start_date,
            "end_date": order_id.end_date,
            "address": order_id.address,
            "price": order_id.price,
            "customer_id": order_id.customer_id,
            "executor_id": order_id.executor_id,
        })
    elif request.method == 'PUT':
        update_data = request.get_json()
        order_id = Order.query.get(id)
        order_id.name = update_data['name']
        order_id.description = update_data['description']
        order_id.start_date = datetime.strptime(update_data['start_date'], '%m/%d/%Y')
        order_id.end_date = datetime.strptime(update_data['end_date'], '%m/%d/%Y')
        order_id.address = update_data['address']
        order_id.price = update_data['price']
        order_id.customer_id = update_data['customer_id']
        order_id.executor_id = update_data['executor_id']

        db.session.add(order_id)
        db.session.commit()

    elif request.method == 'DELETE':
        order_delete = Order.query.get(id)
        db.session.delete(order_delete)
        db.session.commit()

    return '', 200


@app.route('/users', methods=['GET', 'POST'])
def users_index():
    if request.method == 'GET':
        show_users = []
        for user in User.query.all():
            show_users.append({
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "age": user.age,
                "email": user.email,
                "role": user.role,
                "phone": user.phone,
            })
        return jsonify(show_users)

    elif request.method == 'POST':
        data = request.get_json()
        new_user = User(
            id=data['id'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            age=data['age'],
            email=data['email'],
            role=data['role'],
            phone=data['phone'],
        )
        with db.session.begin():
            db.session.add(new_user)
    return '', 200


@app.route('/users/<int:id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def users_index_id(id):
    if request.method == 'GET':
        show_users_id = User.query.get(id)
        return jsonify({
            "id": show_users_id.id,
            "first_name": show_users_id.first_name,
            "last_name": show_users_id.last_name,
            "age": show_users_id.age,
            "email": show_users_id.email,
            "role": show_users_id.role,
            "phone": show_users_id.phone,
        }
        )
    elif request.method == "PUT":
        update_data = request.get_json()
        user_id = User.query.get(id)
        user_id.first_name = update_data['first_name']
        user_id.last_name = update_data['last_name']
        user_id.age = update_data['age']
        user_id.email = update_data['email']
        user_id.role = update_data['role']
        user_id.phone = update_data['phone']

        db.session.add(user_id)
        db.session.commit()

    elif request.method == "DELETE":
        user_delete = User.query.get(id)
        db.session.delete(user_delete)
        db.session.commit()

    return '', 200


@app.route('/offers', methods=['GET', 'POST'])
def offers_index():
    if request.method == 'GET':
        show_offers = []
        for offer in Offer.query.all():
            show_offers.append({
                "id": offer.id,
                "order_id": offer.order_id,
                "executor_id": offer.executor_id,
            })
        return jsonify(show_offers)
    elif request.method == 'POST':
        data = request.get_json()
        new_offer = Offer(
            id=data['id'],
            order_id=data['order_id'],
            executor_id=data['executor_id'],
        )
        with db.session.begin():
            db.session.add(new_offer)
    return '', 200


@app.route('/offers/<int:id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def offers_index_id(id):
    if request.method == 'GET':
        show_offer_id = Offer.query.get(id)
        return jsonify({
            "id": show_offer_id.id,
            "order_id": show_offer_id.order_id,
            "executor_id": show_offer_id.executor_id,
        })
    elif request.method == "PUT":
        update_data = request.get_json()
        offer_id = Offer.query.get(id)
        offer_id.order_id = update_data['order_id']
        offer_id.executor_id = update_data['executor_id']

        db.session.add(offer_id)
        db.session.commit()

    elif request.method == "DELETE":
        offer_delete = Offer.query.get(id)
        db.session.delete(offer_delete)
        db.session.commit()

    return '', 200


if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    get_users_offers_orders()
    app.run(debug=True)
