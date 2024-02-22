from tiktoksellerapi.api import API
from tiktoksellerapi.orders import  Orders


def test_connection():
    api = API()
    # Amsterdam to Berlin
    assert  api.checkenv()


def test_getorder():

    orders = Orders()

    assert len(orders.getOrders(['1729887427421964504','1729887427421964504'])['data']['orders']) > 0