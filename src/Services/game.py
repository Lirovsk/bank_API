from . import db, Utils
from ..app.models import Game


class GameServices:

    @staticmethod
    def search_game(game_uuid: str) -> Game | None:
        return db.session.execute(db.select(Game).filter_by(id=game_uuid)).scalar_one_or_none()

    @staticmethod
    def list_games():
        pass

# Importing PlayerServices here to avoid circular imports. PlayerServices only imports Game model, not GameServices itself, so it won't cause issues. If we imported GameServices in player.py, it would cause a circular import error.
from .player import PlayerServices


class GameCRUD:
    
    @staticmethod
    def create_game(data: dict) -> tuple[dict, int]:
        has_null, null_values = Utils.check_for_null_data(data, "game_used", "bonus_per_round", "start_value")
        if has_null:
            return {"error": f"{null_values} is/are required."}, 400
        
        new_game = Game(game_used=data["game_used"], bonus_per_round=data["bonus_per_round"], start_value=data["start_value"])
        
        try:
            db.session.add(new_game)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500
        
        bank_value = data["start_value"] * 10
        try:
            PlayerServices.create_player(name="Banker", balance=bank_value, game=new_game, bank=True)
        except Exception as e:
            db.session.rollback()
            return {"error": f"Game created but failed to create banker: {str(e)}"}, 500
        
        return {"message": "Game created successfully.", "game_id": new_game.id}, 201
    
    
    @staticmethod
    def delete_game(data: dict) -> tuple[dict, int]:
        has_null, null_values = Utils.check_for_null_data(data, "game_uuid")
        if has_null:
            return {"error": f"{null_values} is required."}, 400
        
        valid_game = GameServices.search_game(data["game_uuid"])
        if not valid_game:
            return {"error": "Game not found."}, 404
        
        try:
            db.session.delete(valid_game)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500
        
        return {"message": "Game deleted successfully."}, 200
    
    
    @staticmethod
    def update_game(data: dict) -> tuple[dict, int]:
        has_null, null_values = Utils.check_for_null_data(data, "game_uuid")
        if has_null:
            return {"error": f"{null_values} is required."}, 400
        
        valid_game = GameServices.search_game(data["game_uuid"])
        if not valid_game:
            return {"error": "Game not found."}, 404
        
        for info in data:
            if hasattr(valid_game, info):
                if info in ["id", "time_of_last_transaction", "number_of_operations", "players"]:
                    continue
                setattr(valid_game, info, data[info])
        
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500
        
        return {"message": "Game updated successfully."}, 200
    
    
    @staticmethod
    def get_game(game_uuid: str) -> tuple[dict, int]:
        valid_game = GameServices.search_game(game_uuid)
        if not valid_game:
            return {"error": "Game not found."}, 404
        
        return {"game": {"id":valid_game.id,
                         "bonus_per_round": valid_game.bonus_per_round,
                         "start_value": valid_game.start_value,
                         "number_of_operations": valid_game.number_of_operations,
                         "number_of_players": len(valid_game.players)}}, 200
