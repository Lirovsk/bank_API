from . import db
from ..app.models import Game, Player
from .utils import Utils
from .game import GameServices


class PlayerServices:

    @staticmethod
    def search_player(player_id: str) -> Player | None:
        return db.session.execute(db.select(Player).filter_by(id=player_id)).scalar_one_or_none()
    
    @staticmethod
    def list_players():
        pass
    
    @staticmethod
    def create_player(name: str, balance: int, game: Game) -> Player:
        new_player = Player(name=name, balance=balance, game=game)
        try:
            db.session.add(new_player)
            db.session.commit()
            return new_player
        except Exception as e:
            db.session.rollback()
            raise e
        
    
    @staticmethod
    def delete_player(player_id: int) -> None:
        player_to_delete = PlayerServices.search_player(player_id)
        if not player_to_delete:
            raise ValueError("Player not found.")
        
        try:
            db.session.delete(player_to_delete)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e


class PlayerCRUD:

    @staticmethod
    def create_player(data: dict, game_uuid: str=None) -> tuple[dict, int]:
        if not game_uuid:
            has_null, null_values = Utils.check_for_null_data(data, "name", "game_uuid")
            if has_null:
                return {"error": f"{null_values} is/are required."}, 400

            game = GameServices.search_game(data["game_uuid"])
            if not game:
                return {"error": "Game not found."}, 404

            balance = game.start_value
            name = data["name"]

            try:
                new_player = PlayerServices.create_player(name, balance, game)
                return {"message": "Player created successfully.", "player_id": new_player.id}, 201
            except Exception as e:
                return {"error": str(e)}, 500

        else:
            has_null, null_values = Utils.check_for_null_data(data, "name")
            if has_null:
                return {"error": f"{null_values} is required."}, 400

            game = GameServices.search_game(game_uuid)
            if not game:
                return {"error": "Game not found."}, 404

            balance = game.start_value
            name = data["name"]

            try:
                new_player = PlayerServices.create_player(name, balance, game)
                return {"message": "Player created successfully.", "player_id": new_player.id}, 201
            except Exception as e:
                return {"error": str(e)}, 500

    @staticmethod
    def delete_player(player_id: int=None, data: dict=None) -> tuple[dict, int]:
        if not player_id:
            has_null, null_values = Utils.check_for_null_data(data, "player_id")
            if has_null:
                return {"error": f"{null_values} is required."}, 400

            player_to_delete = PlayerServices.search_player(data["player_id"])
            if not player_to_delete:
                return {"error": "Player not found."}, 404

            try:
                PlayerServices.delete_player(data["player_id"])
                return {"message": "Player deleted successfully."}, 200
            except Exception as e:
                return {"error": str(e)}, 500

        else:
            player_to_delete = PlayerServices.search_player(player_id)
            if not player_to_delete:
                return {"error": "Player not found."}, 404

            try:
                PlayerServices.delete_player(player_id)
                return {"message": "Player deleted successfully."}, 200
            except Exception as e:
                return {"error": str(e)}, 500

    @staticmethod
    def update_player(data: dict) -> tuple[dict, int]:
        has_null, null_values = Utils.check_for_null_data(data, "player_id")
        if has_null:
            return {"error": f"{null_values} is required."}, 400
        
        player = PlayerServices.search_player(data["player_id"])

        for info in data:
            if hasattr(player, info):
                if info in (
                    "id", "balance", "game", "game_uuid", "transactions_made", "transactions_received", "player_id",):
                    continue
                setattr(player, info, data[info])

        try:
            db.session.commit()
            return {"message": "Player updated successfully."}, 200
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500

    @staticmethod
    def get_player(player_id=None, data: dict=None) -> tuple[dict, int]:
        if not player_id:
            has_null, null_values = Utils.check_for_null_data(data, "player_id")
            if has_null:
                return {"error": f"{null_values} is required."}, 400

            player = PlayerServices.search_player(data["player_id"])
            if not player:
                return {"error": "Player not found."}, 404

            return {"player": {"id": player.id,
                               "name": player.name,
                               "balance": player.balance,
                               "game_uuid": player.game_uuid}}, 200
        else:
            player = PlayerServices.search_player(player_id)
            if not player:
                return {"error": "Player not found."}, 404

            return {"player": {"id": player.id,
                               "name": player.name,
                               "balance": player.balance,
                               "game_uuid": player.game_uuid,
                               "transactions_made": len(player.transactions_made),
                               "transactions_received": len(player.transactions_received)}}, 200 
        

    @staticmethod
    def get_players_by_game(game_uuid: str) -> tuple[dict, int]:
        players = db.session.execute(db.select(Player).filter_by(game_uuid=game_uuid)).scalars().all()
        return {"players": [{"id": player.id,
                             "name": player.name,
                             "balance": player.balance,
                             "game_uuid": player.game_uuid,
                             "transactions_made": len(player.transactions_made),
                             "transactions_received": len(player.transactions_received)} for player in players]}, 200
