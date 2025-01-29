from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

from config import db

# Models go here!
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    role = db.Column(db.String(50), nullable=False)

class Owner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    id_proof = db.Column(db.String(100), nullable=False)
    contact_info = db.Column(db.String(100), nullable=False)

class Buyer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact_info = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(200), nullable=False)
    area = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    owner = db.relationship('Owner', backref='properties', lazy=True)

class LandQuery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'), nullable=False)
    query_text = db.Column(db.Text, nullable=False)
    query_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    user = db.relationship('User', backref='queries', lazy=True)
    property = db.relationship('Property', backref='queries', lazy=True)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('buyer.id'), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('owner.id'), nullable=False)
    transaction_date = db.Column(db.DateTime, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    buyer = db.relationship('Buyer', backref='transactions', lazy=True)
    seller = db.relationship('Owner', backref='sales', lazy=True)

class PropertyTransaction(db.Model):
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'), primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'), primary_key=True)
class Buyer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact_info = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(200), nullable=False)
    area = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    owner = db.relationship('Owner', backref='properties', lazy=True)

class LandQuery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'), nullable=False)
    query_text = db.Column(db.Text, nullable=False)
    query_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    user = db.relationship('User', backref='queries', lazy=True)
    property = db.relationship('Property', backref='queries', lazy=True)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('buyer.id'), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('owner.id'), nullable=False)
    transaction_date = db.Column(db.DateTime, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    buyer = db.relationship('Buyer', backref='transactions', lazy=True)
    seller = db.relationship('Owner', backref='sales', lazy=True)

class PropertyTransaction(db.Model):
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'), primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'), primary_key=True)
