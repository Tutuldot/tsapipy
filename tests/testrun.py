from tiktoksellerapi.api import API
from tiktoksellerapi.orders import  Orders
from tiktoksellerapi.money import Statements

s = Statements()
print(len(s.getStatements(['1729887427421964504','1729887427421964504'])))

