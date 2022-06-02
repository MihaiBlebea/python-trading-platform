from typing import Protocol, List
from src.domain.order.order import Order


class OrderRepo(Protocol):

	def create_table(self)-> None:
		pass

	def find_by_id(self, id: str)-> Order | None:
		pass

	def find_by_status(self, status: str)-> List[Order]:
		pass

	def save(self, order: Order)-> Order:
		pass

	def update_status(self, order: Order)-> None:
		pass