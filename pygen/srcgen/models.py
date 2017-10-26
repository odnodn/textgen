from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
import enum

Model = declarative_base()

class Status(enum.Enum):
    RCVD = 'Rcvd'
    ORDRD = 'Ordrd'
    DLVRD = 'Dlvrd'



class Customer(db.Model):
    __tablename__ = 'Customer'
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String, nullable=False ,)
    lastName = db.Column(db.String, nullable=False ,)
    email = db.Column(db.String, nullable=False ,)

    orders = db.relationship('CustOrder', )

    def __repr__(self):
        return '<Customer %r>' % self.username


class Product(db.Model):
    __tablename__ = 'Product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False ,)
    price = db.Column(db.Numeric, nullable=False ,)


    def __repr__(self):
        return '<Product %r>' % self.username


class Category(db.Model):
    __tablename__ = 'Category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False ,)


    def __repr__(self):
        return '<Category %r>' % self.username


class CustOrder(db.Model):
    __tablename__ = 'CustOrder'
    id = db.Column(db.Integer, primary_key=True)
    notes = db.Column(db.Text, nullable=True ,)
    customer_id = db.Column(db.Integer, db.ForeignKey('Customer.id'))
    dateDelivered = db.Column(db.Date, nullable=False ,)
    isValid = db.Column(db.Boolean, nullable=False ,)
    status = db.Column(db.Enum(Status), nullable=False ,)

    customer = db.relationship('Customer', )
    items = db.relationship('Item',back_populates='custOrder', )

    def __repr__(self):
        return '<CustOrder %r>' % self.username


class Item(db.Model):
    __tablename__ = 'Item'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('Product.id'))
    qty = db.Column(db.Integer, nullable=True ,default=1)
    custOrder_id = db.Column(db.Integer, db.ForeignKey('CustOrder.id'))

    product = db.relationship('Product', )
    custOrder = db.relationship('CustOrder', )

    def __repr__(self):
        return '<Item %r>' % self.username

