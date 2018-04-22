from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
import enum

Model = declarative_base()




class Status(enum.Enum):
    RCVD = 'Rcvd'
    ORDRD = 'Ordrd'
    DLVRD = 'Dlvrd'



class Person:
    firstName = Column(String, nullable=False ,)
    lastName = Column(String, nullable=False ,)
    
    def __repr__(self):
            return '<Person %r>' % self.firstName


class Customer(Model, Person):
    __tablename__ = 'Customer'
    id = Column(Integer, primary_key=True)

    email = Column(String, nullable=False ,)
    
    orders = relationship('CustOrder', )
    def __repr__(self):
            return '<Customer %r>' % self.orders


class Product(Model, ):
    __tablename__ = 'Product'
    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False ,)
    price = Column(Numeric, nullable=False ,)
    
    def __repr__(self):
            return '<Product %r>' % self.name


class Category(Model, ):
    __tablename__ = 'Category'
    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False ,)
    
    def __repr__(self):
            return '<Category %r>' % self.name


class CustOrder(Model, ):
    __tablename__ = 'CustOrder'
    id = Column(Integer, primary_key=True)

    notes = Column(Text, nullable=True ,)
    dateDelivered = Column(Date, nullable=False ,)
    isValid = Column(Boolean, nullable=False ,)
    status = Column(Enum(Status), nullable=False ,)
    customer_id = Column(Integer, ForeignKey('Customer.id'))
    
    customer = relationship('Customer', )
    items = relationship('Item',back_populates='custOrder', )
    def __repr__(self):
            return '<CustOrder %r>' % self.notes


class Item(Model, ):
    __tablename__ = 'Item'
    id = Column(Integer, primary_key=True)

    qty = Column(Integer, nullable=True ,default=1)
    product_id = Column(Integer, ForeignKey('Product.id'))
    custOrder_id = Column(Integer, ForeignKey('CustOrder.id'))
    
    product = relationship('Product', )
    custOrder = relationship('CustOrder', )
    def __repr__(self):
            return '<Item %r>' % self.product




