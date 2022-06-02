import sqlite3
from pathlib import Path
from src.domain.position.position import Position

CWD = Path(__file__).parent.resolve()

class PositionRepoLocal:

	def __init__(self) -> None:
		self.con = sqlite3.connect(f"{CWD}/../../../local.db")
		self.con.row_factory = sqlite3.Row

		self.create_table()
	
	def create_table(self)-> None:
		cur = self.con.cursor() 
		cur.execute("""
			CREATE TABLE IF NOT EXISTS positions
			(
				id VARCHAR(255) PRIMARY KEY,
				symbol VARCHAR(255) NOT NULL,
				quantity INTEGER NOT NULL,
				created_at VARCHAR(255) NOT NULL
			)""")
		self.con.commit()

	def find_by_symbol(self, symbol: str)-> Position | None:
		cur = self.con.cursor()
		record = cur.execute(f"SELECT * FROM positions WHERE symbol = '{symbol}'").fetchone()
		if record is None:
			return None

		return Position(
			record["symbol"],
			record["quantity"],
			record["created_at"],
			record["id"]
		)

	def save(self, position: Position)-> Position:
		cur = self.con.cursor()
		cur.execute("""
			INSERT INTO positions VALUES (?, ?, ?, ?)""", (
				position.id,
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