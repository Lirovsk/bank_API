from ..app import db
from ..app.models import Transaction, Player, Game
from ..Services.transaction import TransactionCRUD

from flask import Blueprint, request


app = Blueprint("transaction", __name__, url_prefix="/transactions")



# ==================== routes ====================#
@app.route("/create", methods=["POST"])
def create_transaction():
    data = request.get_json()
    return TransactionCRUD.create_transaction_for_endpoint(data)


@app.route("/get/<int:transaction_id>", methods=["GET"])
def get_transaction(transaction_id: int):
    return TransactionCRUD.get_transaction_by_id(transaction_id)

@app.route("/get_by_game/<string:game_uuid>", methods=["GET"])
def get_transactions_by_game(game_uuid: str):
    return TransactionCRUD.get_transaction_by_game(game_uuid)


@app.route("/get_by_player/<int:player_id>", methods=["GET"])
def get_transactions_by_player(player_id: int):
    return TransactionCRUD.get_transaction_by_player(player_id)
