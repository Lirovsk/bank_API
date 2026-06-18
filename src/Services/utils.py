from ..models import Game, Player
from . import db

class Utils:
    
    @staticmethod
    def check_for_null_data(data: dict, *args) -> tuple[bool, str]:
        values = []
        has_null = False
        for arg in args:
            value = data.get(arg, None)
            if value is None:
                has_null = True
                values.append(arg)
        return has_null, ", ".join(values)
    
    
    @staticmethod
    def check_game_exists(game_uuid: str) -> Game:
        game = db.session.execute(db.select(Game).filter_by(id=game_uuid)).scalar_one_or_none()
        if not game:
            raise ValueError("Game not found.")
        return game
