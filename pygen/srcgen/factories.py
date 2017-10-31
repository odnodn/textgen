import factory
import factory.alchemy
from datetime import datetime

from pygen.srcgen import common
from . import models

from faker import Faker
faker = Faker()



class CustomerFactory (factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Customer
        sqlalchemy_session = common.Session

    firstName = factory.Sequence(lambda n: "Customer-firstName %d" % n)
    
    lastName = factory.Sequence(lambda n: "Customer-lastName %d" % n)
    
    email = factory.Sequence(lambda n: "Customer-email %d" % n)
    


class ProductFactory (factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Product
        sqlalchemy_session = common.Session

    name = factory.Sequence(lambda n: "Product-name %d" % n)
    
    price = factory.Sequence(lambda n:  n)
    


class CategoryFactory (factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Category
        sqlalchemy_session = common.Session

    name = factory.Sequence(lambda n: "Category-name %d" % n)
    


class CustOrderFactory (factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.CustOrder
        sqlalchemy_session = common.Session

    notes = faker.sentence()
    
    dateDelivered = factory.LazyFunction(datetime.now)
    
    isValid = True # always true for now
    
    status = models.Status.RCVD
    


class ItemFactory (factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Item
        sqlalchemy_session = common.Session

    qty = factory.Sequence(lambda n:  n)
    

