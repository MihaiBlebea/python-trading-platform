from src.domain.order.order_repo import OrderRepo
from src.domain.order.order import Order, OrderDirection, OrderStatus, OrderType
from src.domain.account.account_repo import AccountRepo
from src.domain.position.position_repo import PositionRepo


class OrderPlace:

	def __init__(
		self, 
		order_repo: OrderRepo, 
		account_repo: AccountRepo,
		position_repo: PositionRepo) -> None:

		self.order_repo = order_repo
		self.account_repo = account_repo
		self.position_repo = position_repo

	def buy_order(
		self, 
		account_id: str, 
		symbol: str,
		type: str,
		amount: int)-> Order:

		account = self.account_repo.find_by_id(account_id)
		if account is None:
			raise Exception("account not found")

		account.set_pending_balance(amount)
		self.account_repo.update_balance(account)

		order = Order(
			symbol,
			OrderDirection.BUY,
			OrderType.LIMIT,
			OrderStatus.PENDING,
			amount,
		)

		order = self.order_repo.save(order)
		return order.to_response()

	def sell_order(
		self, 
		account_id: str, 
		symbol: str,
		type: str,
		quantity: int)-> Order:

		account = self.account_repo.find_by_id(account_id)
		if account is None:
			raise Exception("account not found")

		position = self.position_repo.find_by_symbol(symbol)
		if position is None:
			raise Exception("no position found")

		if position.quantity < quantity:
			raise Exception("not enough quantity in position")

		order = Order(
			symbol,
			OrderDirection.SELL,
			OrderType.LIMIT,
			OrderStatus.PENDING,
			0,
			quantity
		)

		order = self.order_repo.save(order)
		return order.to_response()
