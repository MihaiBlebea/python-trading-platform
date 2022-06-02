from src.domain.account.account import Account

class AccountRepo:

	def create_table(self)-> None:
		pass

	def find_by_id(self, id: int)-> Account | None:
		pass

	def find_by_token(self, token: str)-> Account | None:
		pass

	def find_by_email(self, email: str)-> Account | None:
		pass

	def save(self, account: Account)-> Account:
		pass

	def update_balance(self, account: Account)-> None:
		pass