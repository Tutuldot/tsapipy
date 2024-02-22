from tiktoksellerapi.api import API
from tiktoksellerapi.orders import  Orders
from tiktoksellerapi.money import Money

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

