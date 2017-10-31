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




    customer = factory.SubFactory(CustomerFactory)


    dateDelivered = factory.LazyFunction(datetime.now)


    isValid = True # always true for now


    status = models.Status.RCVD




class ItemFactory (factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Item
        sqlalchemy_session = common.Session



    product = factory.SubFactory(ProductFactory)
    qty = factory.Sequence(lambda n:  n)




    custOrder = factory.SubFactory(CustOrderFactory)

