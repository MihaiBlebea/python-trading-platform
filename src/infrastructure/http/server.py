from flask import Flask, jsonify, request
from src.di_container import Container


app = Flask(__name__)

API_V1 = "/api/v1"

AUTH_ENDPOINTS = [
	"deposit",
	"withdrawal",
	"order_buy",
	"order_sell",
	"portfolio",
	"orders"
]

@app.before_request
def hook():
	if request.endpoint in AUTH_ENDPOINTS:
		auth = request.headers.get("Authorization")
		if auth is None:
			return jsonify({}), 401

		token = auth.replace("Bearer", "").strip()
		account = Container.account_auth.get_account_with_token(token)
	
		if account is None:
			return jsonify({}), 401

		request.environ["account_id"] = account.id


@app.route(f"{API_V1}/account/register", methods=["POST"])
def register():
	data = request.get_json(silent=True)
	if data is None:
		return jsonify({
			"error": "missing params"
		})
	return Container.account_auth.register(
		data["username"], 
		data["email"], 
		data["password"],
	)

@app.route(f"{API_V1}/account/login", methods=["POST"])
def login():
	data = request.get_json(silent=True)
	if data is None:
		return jsonify({
			"error": "missing params"
		})

	return Container.account_auth.login(
		data["email"], 
		data["password"],
	)

@app.route(f"{API_V1}/account/deposit", methods=["PUT"])
def deposit():
	data = request.get_json(silent=True)
	if data is None:
		return jsonify({
			"error": "missing params"
		})

	account_id = request.environ["account_id"]

	return Container.account_balance.deposit(
		account_id, 
		data["amount"],
	)

@app.route(f"{API_V1}/account/withdrawal", methods=["PUT"])
def withdrawal():
	data = request.get_json(silent=True)
	if data is None:
		return jsonify({
			"error": "missing params"
		})

	account_id = request.environ["account_id"]

	return Container.account_balance.withdrawal(
		account_id, 
		data["amount"],
	)

@app.route(f"{API_V1}/order/buy", methods=["POST"])
def order_buy():
	data = request.get_json(silent=True)
	if data is None:
		return jsonify({
			"error": "missing params"
		})

	account_id = request.environ["account_id"]

	return Container.order_place.buy_order(
		account_id, 
		data["symbol"],
		data["type"],
		data["amount"],
	)

@app.route(f"{API_V1}/order/sell", methods=["POST"])
def order_sell():
	data = request.get_json(silent=True)
	if data is None:
		return jsonify({
			"error": "missing params"
		})

	account_id = request.environ["account_id"]

	return Container.order_place.sell_order(
		account_id, 
		data["symbol"],
		data["type"],
		data["quantity"],
	)

@app.route(f"{API_V1}/portfolio", methods=["GET"])
def portfolio():
	account_id = request.environ["account_id"]

	return Container.portfolio.get_positions(account_id)

@app.route(f"{API_V1}/orders", methods=["GET"])
def orders():
	account_id = request.environ["account_id"]

	return Container.orders.get_account_orders(account_id)

if __name__ == "__main__":
	app.run(host="0.0.0.0", port="8080", debug=True)