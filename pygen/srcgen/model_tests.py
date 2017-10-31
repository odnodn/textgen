import sqlalchemy

from pygen.srcgen import common
from pygen.srcgen.models import *
from pygen.srcgen import factories


def runTests():
    engine = sqlalchemy.create_engine('sqlite:///:memory:', echo=True)
    # It's a scoped_session, and now is the time to configure it.
    common.Session.configure(bind=engine)
    Model.metadata.create_all(engine)



def testCustomer():
    u = factories.CustomerFactory()
    assert([u] == common.Session.query(Customer).all())

def testProduct():
    u = factories.ProductFactory()
    assert([u] == common.Session.query(Product).all())

def testCategory():
    u = factories.CategoryFactory()
    assert([u] == common.Session.query(Category).all())

def testCustOrder():
    u = factories.CustOrderFactory()
    assert([u] == common.Session.query(CustOrder).all())

def testItem():
    u = factories.ItemFactory()
    assert([u] == common.Session.query(Item).all())

runTests()
testCustomer()
testProduct()
testCategory()
testCustOrder()
testItem()
