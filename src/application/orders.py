from typing import List
from src.domain.account.account_repo import AccountRepo
from src.domain.order.order_repo import OrderRepo
from src.domain.order.order import Order


class Orders:

	def __init__(self, account_repo: AccountRepo, order_repo: OrderRepo) -> None:
		self.account_repo = account_repo
		self.order_repo = order_repo

	def get_account_orders(self, account_id: str)-> List[Order]:
		try:
			account = self.account_repo.find_by_id(account_id)
			if account is None:
				raise Exception("account not found")

			orders = self.order_repo.find_by_account_id(account.id)

			return {
				"orders": [order.to_response() for order in orders]
			}

		except Exception as err:
			return {
				"error": f"[account-orders]: {err}"
			}