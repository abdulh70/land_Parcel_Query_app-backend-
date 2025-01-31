from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin


metadata = MetaData()
db = SQLAlchemy(metadata=metadata)
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    queries = db.relationship('LandQuery', backref='user', lazy=True)


class Owner(db.Model):
    __tablename__ = 'owner'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    lands = db.relationship('Land', backref='owner', lazy=True)


class Buyer(db.Model):
    __tablename__ = 'buyer'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    transactions = db.relationship('Transaction', backref='buyer', lazy=True)


class Land(db.Model):
    __tablename__ = 'land'
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(200), nullable=False)
    size = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'), nullable=False)
    transactions = db.relationship('LandTransaction', back_populates='land')
    queries = db.relationship('LandQuery', backref='land', lazy=True)


class Transaction(db.Model):
    __tablename__ = 'transaction'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('buyer.id'), nullable=False)
    lands = db.relationship('LandTransaction', back_populates='transaction')


class LandTransaction(db.Model):
    __tablename__ = 'land_transaction'
    id = db.Column(db.Integer, primary_key=True)
    land_id = db.Column(db.Integer, db.ForeignKey('land.id'), nullable=False)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'), nullable=False)
    land = db.relationship('Land', back_populates='transactions')
    transaction = db.relationship('Transaction', back_populates='lands')


class LandQuery(db.Model):
    __tablename__ = 'land_query'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    land_id = db.Column(db.Integer, db.ForeignKey('land.id'), nullable=False)
    query_text = db.Column(db.Text, nullable=False)