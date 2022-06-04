from threading import Thread
import math
from src.domain.order.order import Order, OrderStatus
from src.domain.order.order_repo import OrderRepo
from src.domain.position.position_repo import PositionRepo
from src.domain.position.position import Position
from src.domain.order.price_getter import PriceGetter
from src.infrastructure.logger.logger import Logger

class OrderFill:

	def __init__(
		self, 
		order_repo: OrderRepo, 
		position_repo: PositionRepo,
		price_getter: PriceGetter,
		logger: Logger)-> None:

		self.order_repo = order_repo
		self.position_repo = position_repo
		self.price_getter = price_getter
		self.logger = logger

	def execute_single(self, order: Order)-> None:
		(bid, ask) = self.price_getter.get_symbol_price(order.symbol)

		if order.is_sell():
			# bid
			if order.quantity == 0:
				self.logger.log("error", "sell order quantity is 0")
				return
	
			total_price = bid * order.quantity
			order.amount = total_price
		else:
			# ask
			if order.amount == 0:
				self.logger.log("error", "buy order amount is 0")
				return

			total_shares = math.floor(order.amount / ask)
			order.quantity = total_shares

		order.status = OrderStatus.FILLED.value
		self.order_repo.update_status(order)

		position = self.position_repo.find_by_symbol(order.symbol)
		if position is None:
			position = Position(order.account_id, order.symbol, order.quantity)
			self.position_repo.save(position)
		else:
			position.increment_quantity(order.quantity)
			self.position_repo.update_quantity(position)

	def execute_all_pending(self)-> None:
		[
			self.execute_single(order) 
			for order in self.order_repo.find_by_status(OrderStatus.PENDING.value)
		]

	def execute_all_pending_async(self)-> None:
		threads = []
		for order in self.order_repo.find_by_status(OrderStatus.PENDING.value):
			threads.append(
				Thread(target=self.execute_single, args=[order]),
			)
			threads[-1].start()

		for t in threads:
			t.join()

