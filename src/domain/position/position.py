from dataclasses import dataclass
from datetime import datetime
import uuid


@dataclass
class Position:

	symbol: str

	quantity: int

	created_at: datetime = None

	id: str = None

	def __post_init__(self):
		if self.id is None:
			self.id = str(uuid.uuid4())

		if self.created_at is None:
			self.created_at = datetime.now()

		if isinstance(self.created_at, str):
			self.created_at = datetime.strptime(self.created_at, "%m/%d/%Y, %H:%M:%S")

	def to_response(self)-> dict:
		return {
			"id": self.id,
			"symbol": self.symbol,
			"quantity": self.quantity,
			"created_at": self.get_created_str()
		}

	def get_created_str(self)-> str:
		return self.created_at.strftime("%m/%d/%Y, %H:%M:%S")
