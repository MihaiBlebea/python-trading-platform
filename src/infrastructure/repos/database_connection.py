from typing import Protocol


class DatabaseConnection(Protocol):

	def get_connection(self):
		pass
