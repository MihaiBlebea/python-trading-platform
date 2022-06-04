from typing import List
from src.domain.position.position import Position
from src.domain.position.position_repo import PositionRepo
from src.domain.account.account_repo import AccountRepo

class Portfolio:

	def __init__(self, account_repo: AccountRepo, position_repo: PositionRepo)-> None:
		self.account_repo = account_repo
		self.position_repo = position_repo

	def get_positions(self, account_id: str)-> List[Position]:
		try:
			account = self.account_repo.find_by_id(account_id)
			if account is None:
				raise Exception("account not found")

			positions = self.position_repo.find_by_account_id(account.id)
			return {
				"positions": [ position.to_response() for position in positions ]
			}

		except Exception as err:
			return {
				"error": f"[porfolio-positions]: {err}"
			}
		