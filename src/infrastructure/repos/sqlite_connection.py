from pathlib import Path
import sqlite3

CWD = Path(__file__).parent.resolve()

class SqliteConnection:

	def get_connection(self):
		conn = sqlite3.connect(f"{CWD}/../../../data/local.db")
		conn.row_factory = sqlite3.Row

		return conn