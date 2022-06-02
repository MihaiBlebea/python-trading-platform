from crypt import methods
from flask import Flask, jsonify, request
from src.di_container import Container


app = Flask(__name__)

API_V1 = "/api/v1"

AUTH_ENDPOINTS = [
	"deposit",
	"withdrawal"
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

if __name__ == "__main__":
	app.run(host="0.0.0.0", port="8080", debug=True)