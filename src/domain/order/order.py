
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import uuid

class OrderDirection(Enum):
	BUY = "buy"
	SELL = "sell"

class OrderType(Enum):
	MARKET = "market"
	LIMIT = "limit"

class OrderStatus(Enum):
	PENDING = "pending"
	FILLED = "filled"
	CANCELLED = "cancelled"


@dataclass
class Order:

	direction: str

	type: str

	status: str

	amount: int

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
			"direction": self.direction,
			"type": self.type,
			"status": self.status,
			"created_at": self.get_created_str()
		}

	def get_created_str(self)-> str:
		return self.created_at.strftime("%m/%d/%Y, %H:%M:%S")

	def is_status_pending(self)-> bool:
		return self.status == OrderStatus.PENDING
