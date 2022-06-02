from src.domain.account.account_repo import AccountRepo
from src.domain.account.account import Account


class AccountBalance:

	def __init__(self, account_repo: AccountRepo) -> None:
		self.account_repo = account_repo

	def deposit(self, account_id: str, amount: int)-> dict:
		try:
			account = self.account_repo.find_by_id(account_id)
			account.deposit(amount)

			self.account_repo.update_balance(account)

			return account.to_response()
		except Exception as err:
			return {
				"error": f"[account_deposit]: {str(err)}"
			}

	def withdrawal(self, account_id: str, amount: int)-> dict:
		try:
			account = self.account_repo.find_by_id(account_id)
			account.withdrawal(amount)

			self.account_repo.update_balance(account)

			return account.to_response()
		except Exception as err:
			return {
				"error": f"[account_withdrawal]: {str(err)}"
			}