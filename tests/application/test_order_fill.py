from typing import Tuple
import unittest
import math
import sqlite3
from src.domain.account.account import Account
from src.di_container import Container
from src.domain.order.order import (
	Order, 
	OrderDirection, 
	OrderType, 
	OrderStatus
)

# in pounds
BID = 1.22
ASK = 1.28

## Setup mocks in container
class PriceGetterMock:
	
	def get_symbol_price(self, _)-> Tuple[float, float]:
		return (BID, ASK,)


class SqliteInMemoryConnection:

	def get_connection(self):
		conn = sqlite3.connect("file::memory:?cache=shared")
		conn.row_factory = sqlite3.Row

		return conn


class TestContainer(Container):
	price_getter = PriceGetterMock
	database_connection = SqliteInMemoryConnection



class TestOrderFill(unittest.TestCase):

	account = Account("mihai", "mihai@gmail.com", "intrex", 10000)

	@classmethod
	def setUp(self):
		TestContainer.account_repo.create_table()
		TestContainer.account_repo.save(self.account)

	@classmethod
	def tearDown(self):
		TestContainer.account_repo.drop_table()

	def test_can_execute_buy_order(self):
		amount = 2000 # in penny
		quantity_after_fill = 15
		order = Order(self.account.id, "AAPL", "buy", "limit", "pending", amount)
		TestContainer.order_fill.execute_single(order)

		self.assertEqual(order.symbol, "AAPL")
		self.assertEqual(order.direction, OrderDirection.BUY.value)
		self.assertEqual(order.type, OrderType.LIMIT.value)
		self.assertEqual(order.status, OrderStatus.FILLED.value)
		self.assertEqual(order.amount, amount)
		self.assertEqual(order.quantity, quantity_after_fill)

	def test_can_execute_sell_order(self):
		quantity = 12
		order = Order(self.account.id, "AAPL", "sell", "limit", "pending", 0, quantity)
		TestContainer.order_fill.execute_single(order)

		self.assertEqual(order.symbol, "AAPL")
		self.assertEqual(order.direction, OrderDirection.SELL.value)
		self.assertEqual(order.type, OrderType.LIMIT.value)
		self.assertEqual(order.status, OrderStatus.FILLED.value)
		self.assertEqual(order.amount, 1464)
		self.assertEqual(order.quantity, quantity)



if __name__ == "__main__":
    unittest.main()