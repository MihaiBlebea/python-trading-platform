from dependencies import Injector
from src.application import (
	AccountAuth, 
	AccountBalance, 
	OrderPlace,
	OrderFill,
	Portfolio,
	Orders
)
from src.infrastructure.repos import (
	AccountRepoLocal,
	OrderRepoLocal,
	PositionRepoLocal
)
from src.infrastructure.clients.price_getter import PriceGetter
from src.infrastructure.repos.sqlite_connection import SqliteConnection
from src.infrastructure.logger.logger import Logger


class Container(Injector):
	account_auth = AccountAuth
	account_balance = AccountBalance
	order_place = OrderPlace
	order_fill = OrderFill
	account_repo = AccountRepoLocal
	order_repo = OrderRepoLocal
	position_repo = PositionRepoLocal
	price_getter = PriceGetter
	database_connection = SqliteConnection
	logger = Logger
	portfolio = Portfolio
	orders = Orders
