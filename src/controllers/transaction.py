from ..app import db
from ..app.models import Transaction, Player, Game

from flask import Blueprint, request


app = Blueprint("transaction", __name__, url_prefix="/transactions")


class TransactionServices:

    @staticmethod
    def check_for_null_data(data: dict, *args) -> None:
        values = ""
        have_none = False
        for arg in args:
            if data[arg] is None:
                values += f"{arg}, "
                have_none = True
        if have_none:
            raise ValueError(f"{values[:-2]} are required.")

    @staticmethod            
    def check_transaction_type(transaction_type: str) -> None:
        if transaction_type not in ("transfer", "bonus"):
            raise ValueError("transaction_type must be either 'transfer' or 'bonus'.")

    @staticmethod
    def check_game_exists(game_uuid: str) -> Game:
        game = db.session.execute(db.select(Game).filter_by(id=game_uuid)).scalar_one_or_none()
        if not game:
            raise ValueError("Game not found.")

        return game

    @staticmethod
    def check_info_before_transfer(sender: Player, recipient: Player, value: int, game: Game) -> bool:
        if not sender or not recipient:
            raise ValueError("Both sender and recipient must be valid players for a transfer.")

        if sender.game_uuid != game.id or recipient.game_uuid != game.id:
            raise ValueError("Both sender and recipient must belong to the same game.")

        if sender.balance < value:
            raise ValueError("Sender does not have sufficient balance for the transfer.")

class PlayerServices:
    
    @staticmethod
    def check_player_exists(player_id: int, role: str = "player") -> Player:
        player = db.session.execute(db.select(Player).filter_by(id=player_id)).scalar_one_or_none()
        if not player:
            raise ValueError(f"{role.capitalize()} not found.")
        
        return player


# ==================== routes ====================#
@app.route("/create", methods=["POST"])
def create_transaction():
    data = request.get_json()
    
    treated_data = {
        "transaction_type": data.get("transaction_type", None),
        "value": data.get("value", None),
        "game_uuid": data.get("game_uuid", None),
        "sender_id": data.get("sender_id", None),
        "recipient_id": data.get("recipient_id", None)
    }
    
    try: 
        if treated_data["transaction_type"] == "transfer":
            TransactionServices.check_for_null_data(treated_data, "transaction_type", "value", "game_uuid", "sender_id", "recipient_id")
        else: 
            TransactionServices.check_for_null_data(treated_data, "transaction_type", "value", "game_uuid", "sender_id")
            
        TransactionServices.check_transaction_type(treated_data["transaction_type"])
    except ValueError as e:
        return {"error": str(e)}, 400

    try:
        game = TransactionServices.check_game_exists(treated_data["game_uuid"])
    except ValueError as e:
        return {"error": str(e)}, 404
    
    try:
        sender = PlayerServices.check_player_exists(treated_data["sender_id"], "sender")
        if treated_data["transaction_type"] == "transfer":
            recipient = PlayerServices.check_player_exists(treated_data["recipient_id"], "recipient")
        else:
            recipient = None
            
    except ValueError as e:
        return {"error": str(e)}, 404

    if treated_data["transaction_type"] == "transfer":
        try:
            TransactionServices.check_info_before_transfer(sender, recipient, treated_data["value"], game)
        except ValueError as e:
            return {"error": str(e)}, 400
    
    new_transaction = Transaction(transaction_type=treated_data["transaction_type"], value=treated_data["value"], game_uuid=treated_data["game_uuid"], sender=sender, recipient=recipient)
    
    try:
        db.session.add(new_transaction)
        
        # Update balances for transfer transactions
        if treated_data["transaction_type"] == "transfer":
            sender.balance -= treated_data["value"]
            recipient.balance += treated_data["value"]
        
        db.session.commit()
        
    except ValueError as e:
        db.session.rollback()
        return {"error": str(e)}, 500

    return {"message": "Transaction created successfully.", "transaction_id": new_transaction.id}, 201


@app.route("/get/<int:transaction_id>", methods=["GET"])
def get_transaction(transaction_id: int):
    transaction = db.session.execute(db.select(Transaction).filter_by(id=transaction_id)).scalar_one_or_none()
    if not transaction:
        return {"error": "Transaction not found."}, 404

    return {
        "transaction": {
            "id": transaction.id,
            "transaction_type": transaction.transaction_type,
            "value": transaction.value,
            "game_uuid": transaction.game_uuid,
            "sender": transaction.sender.name,
            "recipient": transaction.recipient.name,
            "sender_id": transaction.sender_id,
            "recipient_id": transaction.recipient_id,
        }
    }, 200


@app.route("/get_by_game/<string:game_uuid>", methods=["GET"])
def get_transactions_by_game(game_uuid: str):
    transactions = db.session.execute(db.select(Transaction).filter_by(game_uuid=game_uuid)).scalars().all()
    if not transactions:
        return {"error": "No transactions found for the specified game."}, 404

    return {
        "transactions": [
            {
                "id": tx.id,
                "transaction_type": tx.transaction_type,
                "value": tx.value,
                "game_uuid": tx.game_uuid,
                "sender": tx.sender.name,
                "recipient": tx.recipient.name,
                "sender_id": tx.sender_id,
                "recipient_id": tx.recipient_id,
            }
            for tx in transactions
        ]
    }, 200


@app.route("/get_by_player/<int:player_id>", methods=["GET"])
def get_transactions_by_player(player_id: int):
    transactions = db.session.execute(db.select(Transaction).filter((Transaction.sender_id == player_id) | (Transaction.recipient_id == player_id))).scalars().all()
    if not transactions:
        return {"error": "No transactions found for the specified player."}, 404

    return {"transactions": [{"id": tx.id,
                              "transaction_type": tx.transaction_type,
                              "value": tx.value,
                              "game_uuid": tx.game_uuid,
                              "sender_id": tx.sender_id,
                              "sender": tx.sender.name,
                              "recipient": tx.recipient.name,
                              "recipient_id": tx.recipient_id} for tx in transactions]}, 200
