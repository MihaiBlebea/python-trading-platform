from __future__ import annotations
from typing import Tuple
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import uuid
import math
from src.domain.position.position import Position
from src.domain.account.account import Account


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

	account_id: str

	symbol: str

	direction: str

	type: str

	status: str

	amount: int

	quantity: int = 0

	created_at: datetime = None

	id: str = None

	def __post_init__(self):
		if self.id is None:
			self.id = str(uuid.uuid4())

		if self.created_at is None:
			self.created_at = datetime.now()

		if isinstance(self.created_at, str):
			self.created_at = datetime.strptime(self.created_at, "%m/%d/%Y, %H:%M:%S")

		if isinstance(self.direction, OrderDirection):
			self.direction = self.direction.value

		if isinstance(self.type, OrderType):
			self.type = self.type.value

		if isinstance(self.status, OrderStatus):
			self.status = self.status.value

	def to_response(self)-> dict:
		return {
			"id": self.id,
			"symbol": self.symbol,
			"direction": self.direction,
			"type": self.type,
			"status": self.status,
			"amount": self.amount,
			"quantity": self.quantity,
			"created_at": self.get_created_str()
		}

	def get_created_str(self)-> str:
		return self.created_at.strftime("%m/%d/%Y, %H:%M:%S")

	def is_status_pending(self)-> bool:
		return self.status == OrderStatus.PENDING.value

	def is_sell(self)-> bool:
		return self.direction == OrderDirection.SELL.value

	def fill_buy_order(
		self, 
		ask_price: float,
		account: Account,
		position: Position = None)-> Tuple[Order, Position, Account]:

		if self.amount == 0:
			raise Exception("buy order amount is 0")
		
		ask_price_int = ask_price * 100
		self.quantity = math.floor(self.amount / ask_price_int)
		self.status = OrderStatus.FILLED.value

		if position is None:
			position = Position(self.account_id, self.symbol, self.quantity)
		else:
			position.increment_quantity(self.quantity)

		account.free_pending_balance(self.quantity * ask_price_int)

		return (self, position, account)

	def fill_sell_order(
		self,
		bid_price: float,
		position: Position = None)-> Tuple[Order, Position]:

		if self.quantity == 0:
			raise Exception("sell order quantity is 0")

		bid_price_int = bid_price * 100
		self.amount = bid_price_int * self.quantity
		
		self.status = OrderStatus.FILLED.value

		if position is None:
			position = Position(self.account_id, self.symbol, self.quantity)
		else:
			position.increment_quantity(self.quantity)

		return (self, position)