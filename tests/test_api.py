from tiktoksellerapi.api import API
from tiktoksellerapi.orders import  Orders
from tiktoksellerapi.money import Money
from tiktoksellerapi.product import Product

def test_connection():
    api = API()
    # Amsterdam to Berlin
    assert  api.checkenv()


def test_getorder():

    orders = Orders()

    assert len(orders.getOrders(['1729887427421964504','1729887427421964504'])['data']['orders']) > 0


def test_getstatements():
    s = Money()
    assert len(s.getStatements(['1729887427421964504','1729887427421964504'])) > 0

def test_getpayments():
    s = Money()
    assert len(s.getPayments(['1729887427421964504','1729887427421964504'])) > 0

def test_getsku():
    s = Product()
    assert len(s.getSKU([ "1729887427421964504"])) > 0


    

def test_getproductinfo():
    s = Product()
    assert len(s.getProduct("1729831045943560408")) > 0

