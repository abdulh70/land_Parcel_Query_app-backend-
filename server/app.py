#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, User, Owner, Land,Buyer,Transaction,LandQuery,LandTransaction
from datetime import datetime

# initializing the Flask application
app = Flask(__name__)
# Configuring the database URI and turning off modification tracking
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///land_query.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# Ensuring JSON responses aren't compacted
app.json.compact = False

# Initializing the database and migration objects
db.init_app(app)
migrate = Migrate(app, db)
api=Api(app)

class UserResource(Resource):
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return jsonify({'id': user.id, 'name': user.name, 'email': user.email})
    
    def post(self):
        data = request.get_json()
        if 'name' not in data or 'email' not in data:
            return jsonify({'message': 'Missing required fields: name, email'}), 400
        new_user = User(name=data['name'], email=data['email'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'})
api.add_resource(UserResource, '/users', '/users/<int:user_id>')

class OwnerResource(Resource):
    def get(self, owner_id):
        owner = Owner.query.get_or_404(owner_id)
        return jsonify({'id': owner.id, 'name': owner.name})
    
    def post(self):
        data = request.get_json()
        if 'name' not in data:
            return jsonify({'message': 'Missing required field: name'}), 400
        new_owner = Owner(name=data['name'])
        db.session.add(new_owner)
        db.session.commit()
        return jsonify({'message': 'Owner created successfully'})
api.add_resource(OwnerResource, '/owners', '/owners/<int:owner_id>')

class BuyerResource(Resource):
    def get(self, buyer_id):
        buyer = Buyer.query.get_or_404(buyer_id)
        return jsonify({'id': buyer.id, 'name': buyer.name, 'email': buyer.email})
    
    def post(self):
        data = request.get_json()
        if 'name' not in data or 'email' not in data:
            return jsonify({'message': 'Missing required fields: name, email'}), 400
        new_buyer = Buyer(name=data['name'], email=data['email'])
        db.session.add(new_buyer)
        db.session.commit()
        return jsonify({'message': 'Buyer created successfully'})
api.add_resource(BuyerResource, '/buyers', '/buyers/<int:buyer_id>')

class LandResource(Resource):
    def get(self, land_id):
        land = Land.query.get_or_404(land_id)
        return jsonify({
            'id': land.id, 
            'location': land.location, 
            'size': land.size,
            'owner': {'id': land.owner.id, 'name': land.owner.name}  
        })
 
    def post(self):
        data = request.get_json()
        if 'location' not in data or 'size' not in data or 'owner_id' not in data:
            return jsonify({'message': 'Missing required fields: location, size, owner_id'}), 400
        new_land = Land(location=data['location'], size=data['size'], owner_id=data['owner_id'])
        db.session.add(new_land)
        db.session.commit()
        return jsonify({'message': 'Land created successfully'})
api.add_resource(LandResource, '/lands', '/lands/<int:land_id>')

class LandQueryResource(Resource):
    def post(self):
        data = request.get_json()
        if 'user_id' not in data or 'land_id' not in data or 'query_text' not in data:
            return jsonify({'message': 'Missing required fields: user_id, land_id, query_text'}), 400
        new_query = LandQuery(user_id=data['user_id'], land_id=data['land_id'], query_text=data['query_text'])
        db.session.add(new_query)
        db.session.commit()
        return jsonify({'message': 'Query submitted successfully'})
api.add_resource(LandQueryResource, '/land_queries')


### New Resource: TransactionResource ###
class TransactionResource(Resource):
    def get(self, transaction_id):
        # Fetch the transaction by its ID, or return 404 if not found
        transaction = Transaction.query.get_or_404(transaction_id)

        # Fetch the buyer from the associated buyer_id
        buyer = {
            'id': transaction.buyer.id,
            'name': transaction.buyer.name
        }

        # Fetch associated lands through LandTransaction
        land_transactions = LandTransaction.query.filter_by(transaction_id=transaction.id).all()
        lands = [{'id': lt.land.id, 'location': lt.land.location, 'size': lt.land.size} for lt in land_transactions]

        # Return transaction details, buyer information, and lands associated with the transaction
        return jsonify({
            'transaction_id': transaction.id,
            'buyer': buyer,
            'lands': lands,
            'transaction_date': transaction.date,
            'amount': transaction.amount
        })

    def post(self):
        data = request.get_json()

        # Ensure required fields are present in the request
        if 'buyer_id' not in data or 'land_ids' not in data or 'amount' not in data:
            return jsonify({'message': 'Missing required fields: buyer_id, land_ids, amount'}), 400

        # Create a new transaction
        new_transaction = Transaction(
            buyer_id=data['buyer_id'],
            amount=data['amount'],
            date=datetime.utcnow()
        )
        db.session.add(new_transaction)
        db.session.commit()

        # Link transaction to lands via LandTransaction
        for land_id in data['land_ids']:
            land_transaction = LandTransaction(land_id=land_id, transaction_id=new_transaction.id)
            db.session.add(land_transaction)

        db.session.commit()

        # Return success message
        return jsonify({'message': 'Transaction completed successfully'})

# Add the resource to the API
api.add_resource(TransactionResource, '/transactions', '/transactions/<int:transaction_id>')

### New Resource: TransactionQueryResource ###
class TransactionQueryResource(Resource):
    def post(self):
        data = request.get_json()
        if 'buyer_id' not in data and 'land_id' not in data:
            return jsonify({'message': 'Please provide at least buyer_id or land_id for query'}), 400
        
        # Base query with joins
        query = db.session.query(Transaction).join(Buyer).join(LandTransaction).join(Land).join(Owner)

        # Apply filters if provided
        if 'buyer_id' in data:
            query = query.filter(Transaction.buyer_id == data['buyer_id'])
        
        if 'land_id' in data:
            query = query.filter(Land.id == data['land_id'])

        transactions = query.all()

        if not transactions:
            return jsonify({'message': 'No transactions found for the given criteria'}), 404

        result = []
        for transaction in transactions:
            land_transactions = LandTransaction.query.filter_by(transaction_id=transaction.id).all()
            lands = [{'id': lt.land.id, 'location': lt.land.location, 'size': lt.land.size, 
                      'owner': {'id': lt.land.owner.id, 'name': lt.land.owner.name}} for lt in land_transactions]

            result.append({
                'transaction_id': transaction.id,
                'buyer': {'id': transaction.buyer.id, 'name': transaction.buyer.name},
                'lands': lands,
                'transaction_date': transaction.date,
                'amount': transaction.amount
            })

        return jsonify(result)

api.add_resource(TransactionQueryResource, '/transaction_queries')

@app.route('/')
def index():
    return '<h1>Project Server</h1>'


if __name__ == '__main__':
    app.run(port=5555, debug=True)

