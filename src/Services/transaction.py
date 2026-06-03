from . import db
from .player import PlayerServices
from .utils import Utils

from ..app.models import Transaction, Game, Player


class TransactionServices:
    
    @staticmethod
    def check_transaction_type(transaction_type: str):
        valid_types = ["transfer", "deposit"]
        if transaction_type not in valid_types:
            raise ValueError(f"Invalid transaction type. Valid types are: {', '.join(valid_types)}.")
        
        
    @staticmethod
    def check_info_before_transfer(sender: Player, recipient: Player, value: int, game: Game):
        if sender.id == recipient.id:
            raise ValueError("Sender and recipient cannot be the same player.")
        
        if sender.game_uuid != game.id or recipient.game_uuid != game.id:
            raise ValueError("Both sender and recipient must belong to the same game.")
        
        if sender.balance < value:
            raise ValueError("Sender does not have enough balance for this transfer.")
        


class TransactionCRUD:
    
    @staticmethod
    def create_transaction_for_endpoint(data: dict) -> tuple[dict, int]:
        # This method already use the new pattern where the bank player exists
        has_null, missing_values = Utils.check_for_null_data(data, "transaction_type", "value", "game_uuid", "sender_id", "recipient_id")
        if has_null:
            return {"error": f"{missing_values} is/are required."}, 400
        
        try:
            TransactionServices.check_transaction_type(data["transaction_type"])
        except ValueError as e:
            return {"error": str(e)}, 400
        
        game = Utils.check_game_exists(data["game_uuid"])
        if game is None:
            return {"error": "Game not found."}, 404
        
        else:
            sender = PlayerServices.search_player(data["sender_id"])
            recipient = PlayerServices.search_player(data["recipient_id"])
            if None in (sender, recipient):
                if sender is None:
                    return {"error": "Sender not found."}, 404
                else:
                    return {"error": "Recipient not found."}, 404
            
            try:
                TransactionServices.check_info_before_transfer(sender, recipient, data["value"], game)
            except ValueError as e:
                return {"error": str(e)}, 400
            
            new_transaction = Transaction(transaction_type=data["transaction_type"], 
                                          value=data["value"], 
                                          game_uuid=data["game_uuid"], 
                                          sender=sender, 
                                          recipient=recipient)
            try:
                db.session.add(new_transaction)
                sender.balance -= data["value"]
                recipient.balance += data["value"]
                db.session.commit()
                return {"message": "Transfer completed successfully.", "transaction_id": new_transaction.id}, 201
            except Exception as e:
                db.session.rollback()
                return {"error": f"An error occurred while creating the transaction: {str(e)}"}, 500
    
    
    @staticmethod
    def get_transaction_by_id(transaction_id: int) -> tuple[dict, int]:
        transaction = db.session.execute(db.select(Transaction).filter_by(id=transaction_id)).scalar_one_or_none()
        if not transaction:
            return {"error": "Transaction not found."}, 404
        
        return {"transaction": {
            "id": transaction.id,
            "transaction_type": transaction.transaction_type,
            "value": transaction.value,
            "game_uuid": transaction.game_uuid,
            "sender_id": transaction.sender_id,
            "recipient_id": transaction.recipient_id
        }}, 200
    
    
    @staticmethod
    def get_transaction_by_game(game_uuid: str) -> tuple[dict, int]:
        transactions = db.session.execute(db.select(Transaction).filter_by(game_uuid=game_uuid)).scalars().all()
        if not transactions:
            return {"error": "No transactions found for the specified game."}, 404
        
        return {"transactions": [
            {
                "id": tx.id,
                "transaction_type": tx.transaction_type,
                "value": tx.value,
                "game_uuid": tx.game_uuid,
                "sender_id": tx.sender_id,
                "recipient_id": tx.recipient_id
            } for tx in transactions
        ]}, 200
    
    
    @staticmethod
    def get_transaction_by_player(player_id: int) -> tuple[dict, int]:
        transactions = db.session.execute(db.select(Transaction).filter((Transaction.sender_id == player_id) | (Transaction.recipient_id == player_id))).scalars().all()
        if not transactions:
            return {"error": "No transactions found for the specified player."}, 404
        
        return {"transactions": [
            {
                "id": tx.id,
                "transaction_type": tx.transaction_type,
                "value": tx.value,
                "game_uuid": tx.game_uuid,
                "sender_id": tx.sender_id,
                "recipient_id": tx.recipient_id
            } for tx in transactions
        ]}, 200
        
        
    @staticmethod
    def create_transaction():
        pass
