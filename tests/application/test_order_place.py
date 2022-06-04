import unittest
import sqlite3
from src.domain.account.account import Account
from src.domain.position.position import Position
from src.di_container import Container


## Setup mocks in container
class SqliteInMemoryConnection:

	def get_connection(self):
		conn = sqlite3.connect("file::memory:?cache=shared")
		conn.row_factory = sqlite3.Row

		return conn

class TestContainer(Container):
	database_connection = SqliteInMemoryConnection


class TestOrderPlace(unittest.TestCase):

	account = Account("mihai", "mihai@gmail.com", "intrex", 10000)

	@classmethod
	def setUp(self):
		TestContainer.account_repo.create_table()
		TestContainer.order_repo.create_table()
		TestContainer.position_repo.create_table()
		TestContainer.account_repo.save(self.account)
		TestContainer.position_repo.save(Position(self.account.id, "AAPL", 3))

	@classmethod
	def tearDown(self):
		TestContainer.account_repo.drop_table()
		TestContainer.order_repo.drop_table()
		TestContainer.position_repo.drop_table()

	def test_can_place_limit_buy_order(self):
		amount = 2000
		TestContainer.order_place.buy_order(self.account.id, "AAPL", "limit", amount)
		orders = TestContainer.order_repo.find_by_status("pending")

		self.assertEquals(len(orders), 1)
		pending_order = orders[0]
		
		self.assertEqual(pending_order.symbol, "AAPL")
		self.assertEqual(pending_order.status, "pending")
		self.assertEqual(pending_order.amount, amount)
		self.assertEqual(pending_order.quantity, 0)

	def test_can_place_limit_sell_order(self):
		quantity = 2
		TestContainer.order_place.sell_order(self.account.id, "AAPL", "limit", quantity)
		orders = TestContainer.order_repo.find_by_status("pending")

		self.assertEquals(len(orders), 1)
		pending_order = orders[0]
		
		self.assertEqual(pending_order.symbol, "AAPL")
		self.assertEqual(pending_order.status, "pending")
		self.assertEqual(pending_order.amount, 0)
		self.assertEqual(pending_order.quantity, quantity)


if __name__ == "__main__":
    unittest.main()