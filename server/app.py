#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request
from flask_restful import Resource

# Local imports
from config import app, db, api
# Add your model imports


# Views go here!

@app.route('/')
def index():
    return '<h1>Project Server</h1>'

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///land_query.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/users', methods=['POST'])
    def create_user():
        data = request.json
        user = User(name=data['name'], email=data['email'], phone=data['phone'], role=data['role'])
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User created', 'user': {'id': user.id, 'name': user.name}}), 201

    @app.route('/owners', methods=['POST'])
    def create_owner():
        data = request.json
        owner = Owner(name=data['name'], id_proof=data['id_proof'], contact_info=data['contact_info'])
        db.session.add(owner)
        db.session.commit()
        return jsonify({'message': 'Owner created', 'owner': {'id': owner.id, 'name': owner.name}}), 201

    @app.route('/buyers', methods=['POST'])
    def create_buyer():
        data = request.json
        buyer = Buyer(name=data['name'], contact_info=data['contact_info'], email=data['email'])
        db.session.add(buyer)
        db.session.commit()
        return jsonify({'message': 'Buyer created', 'buyer': {'id': buyer.id, 'name': buyer.name}}), 201

    @app.route('/properties', methods=['POST'])
    def create_property():
        data = request.json
        property = Property(location=data['location'], area=data['area'], owner_id=data['owner_id'], status=data['status'])
        db.session.add(property)
        db.session.commit()
        return jsonify({'message': 'Property created', 'property': {'id': property.id, 'location': property.location}}), 201

    @app.route('/queries', methods=['POST'])
    def create_query():
        data = request.json
        query = LandQuery(user_id=data['user_id'], property_id=data['property_id'], query_text=data['query_text'], query_date=datetime.strptime(data['query_date'], '%Y-%m-%d'), status=data['status'])
        db.session.add(query)
        db.session.commit()
        return jsonify({'message': 'Query created', 'query': {'id': query.id, 'query_text': query.query_text}}), 201

    @app.route('/transactions', methods=['POST'])
    def create_transaction():
        data = request.json
        transaction = Transaction(buyer_id=data['buyer_id'], seller_id=data['seller_id'], transaction_date=datetime.strptime(data['transaction_date'], '%Y-%m-%d'), amount=data['amount'])
        db.session.add(transaction)
        db.session.commit()
        return jsonify({'message': 'Transaction created', 'transaction': {'id': transaction.id, 'amount': transaction.amount}}), 201

    @app.route('/property-transactions', methods=['POST'])
    def create_property_transaction():
        data = request.json
        property_transaction = PropertyTransaction(property_id=data['property_id'], transaction_id=data['transaction_id'])
        db.session.add(property_transaction)
        db.session.commit()
        return jsonify({'message': 'Property-Transaction link created'}), 201

    return app
if __name__ == '__main__':
    app.run(port=5555, debug=True)

