from typing import List
from pathlib import Path
from src.domain.position.position import Position
from src.infrastructure.repos.database_connection import DatabaseConnection


CWD = Path(__file__).parent.resolve()

class PositionRepoLocal:

	def __init__(self, database_connection: DatabaseConnection) -> None:
		self.con = database_connection.get_connection()
		self.create_table()
	
	def create_table(self)-> None:
		cur = self.con.cursor() 
		cur.execute("""
			CREATE TABLE IF NOT EXISTS positions
			(
				id VARCHAR(255) PRIMARY KEY,
				account_id VARCHAR(255) NOT NULL,
				symbol VARCHAR(255) NOT NULL,
				quantity INTEGER NOT NULL,
				created_at VARCHAR(255) NOT NULL
			)""")
		self.con.commit()

	def drop_table(self)-> None:
		cur = self.con.cursor() 
		cur.execute("DROP TABLE positions")
		self.con.commit()

	def find_by_symbol(self, symbol: str)-> Position | None:
		cur = self.con.cursor()
		record = cur.execute(f"SELECT * FROM positions WHERE symbol = '{symbol}'").fetchone()
		if record is None:
			return None

		return self.from_row_to_model(record)

	def find_by_account_id(self, account_id: str)-> List[Position]:
		cur = self.con.cursor()
		records = cur.execute(f"SELECT * FROM positions WHERE account_id = '{account_id}'").fetchall()

		positions = []
		for row in records:
			positions.append(
				self.from_row_to_model(row)
			)

		return positions

	def save(self, position: Position)-> Position:
		cur = self.con.cursor()
		cur.execute("""
			INSERT INTO positions VALUES (?, ?, ?, ?, ?)""", (
				position.id,
				position.account_id,
				position.symbol,
				position.quantity,
				position.get_created_str()
			))

		self.con.commit()

		return position

	def update_quantity(self, position: Position)-> None:
		cur = self.con.cursor()
		cur.execute(f"""
			UPDATE positions
			SET
				quantity = '{position.quantity}'
			WHERE
				id = '{position.id}'
		""")

		self.con.commit()

	def from_row_to_model(self, row: dict)-> Position:
		return Position(
			row["account_id"],
			row["symbol"],
			row["quantity"],
			row["created_at"],
			row["id"]
		)