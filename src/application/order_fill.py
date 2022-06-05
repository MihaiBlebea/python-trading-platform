from threading import Thread
import math
from src.domain.order.order import Order, OrderStatus
from src.domain.order.order_repo import OrderRepo
from src.domain.position.position_repo import PositionRepo
from src.domain.account.account_repo import AccountRepo
from src.domain.order.price_getter import PriceGetter
from src.infrastructure.logger.logger import Logger


class OrderFill:

	def __init__(
		self, 
		order_repo: OrderRepo, 
		position_repo: PositionRepo,
		account_repo: AccountRepo,
		price_getter: PriceGetter,
		logger: Logger)-> None:

		self.order_repo = order_repo
		self.position_repo = position_repo
		self.account_repo = account_repo
		self.price_getter = price_getter
		self.logger = logger

	def execute_single(self, order: Order)-> None:
		(bid, ask) = self.price_getter.get_symbol_price(order.symbol)
		position = self.position_repo.find_by_symbol(order.symbol)
		account = self.account_repo.find_by_id(order.account_id)
		if account is None:
			raise Exception("account not found")

		position_exists = True
		if position is None:
			position_exists = False

		if order.is_sell():
			(order, position) = order.fill_sell_order(bid, position)
		else:
			(order, position, account) = order.fill_buy_order(ask, account, position)
			self.account_repo.update_balance(account)

		if position_exists:
			self.position_repo.update_quantity(position)
		else:
			self.position_repo.save(position)
		
		self.order_repo.update_status(order)

	def execute_all_pending(self)-> None:
		for order in self.order_repo.find_by_status(OrderStatus.PENDING.value):
			try:
				self.execute_single(order)
			except Exception as err:
				self.logger.log("error", str(err))
				continue

	def execute_all_pending_async(self)-> None:
		threads = []
		for order in self.order_repo.find_by_status(OrderStatus.PENDING.value):
			threads.append(
				Thread(target=self.execute_single, args=[order]),
			)
			threads[-1].start()

		for t in threads:
			t.join()

