from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
import enum

Model = declarative_base()

class test:
    1
    2
    3
    4

class Status(enum.Enum):
     RCVD = 'Rcvd'
     ORDRD = 'Ordrd'
     DLVRD = 'Dlvrd'


class Customer(Model):
        __tablename__ = 'Customer'
        id = Column(Integer, primary_key=True)
    firstName = Column(String, nullable=False ,)
    lastName = Column(String, nullable=False ,)
    email = Column(String, nullable=False ,)

        orders = relationship('CustOrder', )

    def __repr__(self):
    return '<Customer %r>' % self.firstName

class Product(Model):
        __tablename__ = 'Product'
        id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False ,)
    price = Column(Numeric, nullable=False ,)


    def __repr__(self):
    return '<Product %r>' % self.name

class Category(Model):
        __tablename__ = 'Category'
        id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False ,)


    def __repr__(self):
    return '<Category %r>' % self.name

class CustOrder(Model):
        __tablename__ = 'CustOrder'
        id = Column(Integer, primary_key=True)
    notes = Column(Text, nullable=True ,)
                customer_id = Column(Integer, 
                ForeignKey('Customer.id'))
    dateDelivered = Column(Date, nullable=False ,)
    isValid = Column(Boolean, nullable=False ,)
    status = Column(Enum(Status), nullable=False ,)

        customer = relationship('Customer', )
        items = relationship('Item',back_populates='custOrder', )

    def __repr__(self):
    return '<CustOrder %r>' % self.notes

class Item(Model):
        __tablename__ = 'Item'
        id = Column(Integer, primary_key=True)
                product_id = Column(Integer, 
                ForeignKey('Product.id'))
    qty = Column(Integer, nullable=True ,default=
                1)
                custOrder_id = Column(Integer, 
                ForeignKey('CustOrder.id'))

        product = relationship('Product', )
        custOrder = relationship('CustOrder', )

    def __repr__(self):
    return '<Item %r>' % self.product

