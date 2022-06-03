from typing import Tuple, List
import unittest
import math
from src.di_container import Container
from src.domain.order.order import (
	Order, 
	OrderDirection, 
	OrderType, 
	OrderStatus
)

BID = 10
ASK = 12

## Setup mocks in container
class PriceGetterMock:
	
	def get_symbol_price(self, _)-> Tuple[float, float]:
		return (BID, ASK,)


class orderRepoMock:

	def find_by_status(self, status: str)-> List[Order]:
		return [
			Order("AAPL", "buy", "limit", "pending", 200),
			Order("GOOGL", "buy", "limit", "pending", 1500),
			Order("TSLA", "sell", "limit", "pending", 700)
		]

	def update_status(self, order: Order)-> None:
		pass


class TestContainer(Container):
	price_getter = PriceGetterMock
	order_repo = orderRepoMock


class TestOrderExecute(unittest.TestCase):

	def test_can_execute_buy_order(self):
		amount = 2000
		quantity_after_fill = math.floor(amount / ASK)
		order = Order("AAPL", "buy", "limit", "pending", amount)
		TestContainer.order_execute.execute_single(order)

		self.assertEqual(order.symbol, "AAPL")
		self.assertEqual(order.direction, OrderDirection.BUY.value)
		self.assertEqual(order.type, OrderType.LIMIT.value)
		self.assertEqual(order.status, OrderStatus.FILLED.value)
		self.assertEqual(order.amount, amount)
		self.assertEqual(order.quantity, quantity_after_fill)

	def test_can_execute_sell_order(self):
		quantity = 12
		order = Order("AAPL", "sell", "limit", "pending", 0, quantity)
		TestContainer.order_execute.execute_single(order)

		self.assertEqual(order.symbol, "AAPL")
		self.assertEqual(order.direction, OrderDirection.SELL.value)
		self.assertEqual(order.type, OrderType.LIMIT.value)
		self.assertEqual(order.status, OrderStatus.FILLED.value)
		self.assertEqual(order.amount, 120)
		self.assertEqual(order.quantity, quantity)

	def test_execute_multiple_orders(self):
		TestContainer.order_execute.execute_all_pending()


if __name__ == "__main__":
    unittest.main()