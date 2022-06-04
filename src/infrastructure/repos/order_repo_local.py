from typing import List
import sqlite3
from pathlib import Path
from src.domain.order.order import Order
from src.infrastructure.repos.database_connection import DatabaseConnection


CWD = Path(__file__).parent.resolve()

class OrderRepoLocal:

	def __init__(self, database_connection: DatabaseConnection) -> None:
		self.con = database_connection.get_connection()
		self.create_table()
	
	def create_table(self)-> None:
		cur = self.con.cursor() 
		cur.execute("""
			CREATE TABLE IF NOT EXISTS orders
			(
				id VARCHAR(255) PRIMARY KEY,
				account_id VARCHAR(255) NOT NULL,
				symbol VARCHAR(255) NOT NULL,
				direction VARCHAR(255) NOT NULL,
				type VARCHAR(255) NOT NULL,
				status VARCHAR(255) NOT NULL,
				amount INTEGER NOT NULL,
				quantity INTEGER NOT NULL,
				created_at VARCHAR(255) NOT NULL
			)""")
		self.con.commit()

	def drop_table(self)-> None:
		cur = self.con.cursor() 
		cur.execute("DROP TABLE orders")
		self.con.commit()

	def find_by_id(self, id: str)-> Order | None:
		cur = self.con.cursor()
		record = cur.execute(f"SELECT * FROM orders WHERE id = '{id}'").fetchone()
		if record is None:
			return None

		return self.from_row_to_model(record)

	def find_by_status(self, status: str)-> List[Order]:
		cur = self.con.cursor()
		records = cur.execute(f"SELECT * FROM orders WHERE status = '{status}'").fetchall()
		
		orders = []
		for row in records:
			orders.append(
				self.from_row_to_model(row)
			)

		return orders

	def find_by_account_id(self, account_id: str)-> List[Order]:
		cur = self.con.cursor()
		records = cur.execute(f"SELECT * FROM orders WHERE account_id = '{account_id}'").fetchall()
		
		orders = []
		for row in records:
			orders.append(
				self.from_row_to_model(row)
			)

		return orders

	def save(self, order: Order)-> Order:
		cur = self.con.cursor()
		cur.execute("""
			INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", (
				order.id,
				order.account_id,
				order.symbol,
				order.direction,
				order.type,
				order.status,
				order.amount,
				order.quantity,
				order.get_created_str()
			))

		self.con.commit()

		return order

	def update_status(self, order: Order)-> None:
		cur = self.con.cursor()
		cur.execute(f"""
			UPDATE orders
			SET
				status = '{order.status}',
				amount = '{order.amount}',
				quantity = '{order.quantity}'
			WHERE
				id = '{order.id}'
		""")

		self.con.commit()

	def from_row_to_model(self, row: dict)-> Order:
		return Order(
			row["account_id"],
			row["symbol"],
			row["direction"],
			row["type"],
			row["status"],
			row["amount"],
			row["quantity"],
			row["created_at"],
			row["id"]
		)