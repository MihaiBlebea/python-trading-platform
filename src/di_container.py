from dependencies import Injector
from src.application import (
	AccountAuth, 
	AccountBalance, 
	OrderPlace,
	OrderExecute
)
from src.infrastructure.repos import (
	AccountRepo,
	AccountRepoLocal,
	OrderRepoLocal,
	PositionRepoLocal
)
from src.infrastructure.clients.price_getter import PriceGetter

ENV = "local"

class Container(Injector):
	account_auth = AccountAuth
	account_balance = AccountBalance
	order_place = OrderPlace
	order_execute = OrderExecute
	account_repo = AccountRepo if ENV == "prod" else AccountRepoLocal
	order_repo = OrderRepoLocal
	position_repo = PositionRepoLocal
	price_getter = PriceGetter
