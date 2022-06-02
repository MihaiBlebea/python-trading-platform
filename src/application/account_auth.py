from src.domain.account.account_repo import AccountRepo
from src.domain.account.account import Account


class AccountAuth:

	def __init__(self, account_repo: AccountRepo) -> None:
		self.account_repo = account_repo

	def register(self, username: str, email: str, password: str)-> dict:
		try:
			account = Account(username, email, password, 10000)
			account = self.account_repo.save(account)

			return account.to_response()
		except Exception as err:
			return {
				"error": f"[account_register]: {str(err)}"
			}

	def login(self, email: str, password: str)-> dict:
		try:
			account = self.account_repo.find_by_email(email)

			if account is None:
				raise Exception("incorrect email")

			if account.check_password(password) == False:
				raise Exception("incorrect password")

			return account.to_response()
		except Exception as err:
			return {
				"error": f"[account_login]: {str(err)}"
			}

	def get_account_with_token(self, token: str)-> Account | None:
		try:
			return self.account_repo.find_by_token(token)
		except:
			return None