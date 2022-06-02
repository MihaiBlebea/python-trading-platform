
from dataclasses import dataclass
from datetime import datetime
import uuid 
import jwt
import bcrypt

JWT_SECRET = "secret"

@dataclass
class Account:

	username: str

	email: str

	password: str

	balance: str

	created_at: datetime = None

	token: str = None

	id: str = None

	def __post_init__(self):
		if self.id is None:
			self.id = str(uuid.uuid4())
		if self.token is None:
			self.token = jwt.encode({"id": self.id}, JWT_SECRET, algorithm="HS256")
		if self.created_at is None:
			self.created_at = datetime.now()
		if isinstance(self.created_at, str):
			self.created_at = datetime.strptime(self.created_at, "%m/%d/%Y, %H:%M:%S")
		if isinstance(self.password, str):
			self.password = self.hash_password(self.password)

	def to_response(self)-> dict:
		return {
			"id": self.id,
			"username": self.username,
			"email": self.email,
			"balance": self.balance,
			"token": self.token,
			"created_at": self.get_created_str()
		}

	def get_created_str(self)-> str:
		return self.created_at.strftime("%m/%d/%Y, %H:%M:%S")

	def hash_password(self, password: str)-> str:
		salt = bcrypt.gensalt()
		b = password.encode("utf-8")

		return bcrypt.hashpw(b, salt)
	
	def check_password(self, password: str)-> bool:
		b = password.encode("utf-8")
		return bcrypt.checkpw(b, self.password)

	def deposit(self, amount: int)-> None:
		self.balance += amount

	def withdrawal(self, amount: int)-> None:
		self.balance -= amount
