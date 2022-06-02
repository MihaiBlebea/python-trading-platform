from dependencies import Injector
from src.application import (
	AccountAuth, 
	AccountBalance, 
	OrderPlace
)
from src.infrastructure.repos import (
	AccountRepo,
	AccountRepoLocal,
	OrderRepoLocal,
	PositionRepoLocal
)

ENV = "local"

class Container(Injector):
	account_auth = AccountAuth
	account_balance = AccountBalance
	order_place = OrderPlace
	account_repo = AccountRepo if ENV == "prod" else AccountRepoLocal
	order_repo = OrderRepoLocal
	position_repo = PositionRepoLocal