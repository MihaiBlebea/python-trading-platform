import sqlite3
from pathlib import Path
from src.domain.account.account import Account
from src.infrastructure.repos.database_connection import DatabaseConnection


CWD = Path(__file__).parent.resolve()

class AccountRepoLocal:

	def __init__(self, database_connection: DatabaseConnection) -> None:
		self.con = database_connection.get_connection()
		self.create_table()
	
	def create_table(self)-> None:
		cur = self.con.cursor() 
		cur.execute("""
			CREATE TABLE IF NOT EXISTS accounts
			(
				id VARCHAR(255) PRIMARY KEY,
				username VARCHAR NOT NULL,
				email VARCHAR(255) NOT NULL UNIQUE,
				password VARCHAR(255) NOT NULL,
				token VARCHAR(255) NOT NULL UNIQUE,
				balance INTEGER NOT NULL,
				pending_balance INTEGER DEFAULT 0,
				created_at VARCHAR(255) NOT NULL
			)""")
		self.con.commit()

	def drop_table(self)-> None:
		cur = self.con.cursor() 
		cur.execute("DROP TABLE accounts")
		self.con.commit()

	def find_by_id(self, id: str)-> Account | None:
		cur = self.con.cursor()
		record = cur.execute(f"SELECT * FROM accounts WHERE id = '{id}'").fetchone()
		if record is None:
			return None

		return Account(
			record["username"],
			record["email"],
			record["password"],
			record["balance"],
			record["pending_balance"],
			record["created_at"],
			record["token"],
			record["id"]
		)

	def find_by_token(self, token: str)-> Account | None:
		cur = self.con.cursor()
		record = cur.execute(f"SELECT * FROM accounts WHERE token = '{token}'").fetchone()
		if record is None:
			return None

		return Account(
			record["username"],
			record["email"],
			record["password"],
			record["balance"],
			record["pending_balance"],
			record["created_at"],
			record["token"],
			record["id"]
		)

	def find_by_email(self, email: str)-> Account | None:
		cur = self.con.cursor()
		record = cur.execute(f"SELECT * FROM accounts WHERE email = '{email}'").fetchone()
		if record is None:
			return None

		return Account(
			record["username"],
			record["email"],
			record["password"],
			record["balance"],
			record["pending_balance"],
			record["created_at"],
			record["token"],
			record["id"]
		)

	def save(self, account: Account)-> Account:
		cur = self.con.cursor()
		cur.execute("""
			INSERT INTO accounts VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", (
				account.id,
				account.username,
				account.email,
				account.password,
				account.token,
				account.balance,
				account.pending_balance,
				account.get_created_str()
			))

		self.con.commit()

		return account

	def update_balance(self, account: Account)-> None:
		cur = self.con.cursor()
		cur.execute(f"""
			UPDATE accounts
			SET
				balance = '{account.balance}',
				pending_balance = '{account.pending_balance}'
			WHERE
				id = '{account.id}'
		""")

		self.con.commit()