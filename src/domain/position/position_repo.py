from typing import Protocol, List
from src.domain.position.position import Position


class PositionRepo(Protocol):

	def create_table(self)-> None:
		pass

	def find_by_symbol(self, symbol: str)-> Position | None:
		pass

	def find_by_account_id(self, id: str)-> List[Position]:
		pass

	def save(self, position: Position)-> Position:
		pass

	def update_quantity(self, position: Position)-> None:
		pass