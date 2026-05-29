from ..app.models import Game
from ..app import db

from flask import Blueprint, request


app = Blueprint("game", __name__, url_prefix="/games")



#==================== routes ====================#
@app.route("/create", methods=["POST"])
def create_game():
    data = request.get_json()
    
    game_used = data.get("game_used", None)
    bonus_per_round = data.get("bonus_per_round", None)
    start_value = data.get("start_value", None)
    
    if None in (game_used, bonus_per_round, start_value):
        values = ""
        for field in ("game_used", "bonus_per_round", "start_value"):
            if data.get(field, None) is None:
                values += f"{field}, "
        
        return {"error": f"{values[:-2]} are required."}, 400
            
        
    
    new_game = Game(game_used=game_used, bonus_per_round=bonus_per_round, start_value=start_value)
    
    try:
        db.session.add(new_game)
        db.session.commit()
        
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

    return {"message": "Game created successfully.", "game_id": new_game.id}, 201


@app.route("/delete", methods=["DELETE"])
def delete_game():
    data = request.get_json()
    game_uuid = data.get("game_uuid", None)
    
    if not game_uuid:
        return {"error": "game_uuid is required."}, 400
    
    game_to_delete = db.session.execute(db.select(Game).filter_by(id=game_uuid)).scalar_one_or_none()
    
    if not game_to_delete:
        return {"error": "Game not found."}, 404
    
    try:
        db.session.delete(game_to_delete)
        db.session.commit()
    
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500
    
    return {"message": "Game deleted successfully."}, 200


@app.route("/update", methods=["PATCH"])
def update_game():
    data = request.get_json()
    
    game_uuid = data.get("game_uuid", None)
    if not game_uuid:
        return {"error": "game_uuid is required."}, 400
    
    game = db.session.execute(db.select(Game).filter_by(id=game_uuid)).scalar_one_or_none()
    if not game:
        return {"error": "Game not found."}, 404
    
    for info in data:
        if hasattr(game, info):
            if info in ("id", "time_of_last_transaction", "number_of_operations", "players"):
                continue
            
            setattr(game, info, data[info])
            
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

    return {"message": "Game updated successfully."}, 200


@app.route("/get/<string:game_uuid>", methods=["GET"])
def get_game(game_uuid):
    game = db.session.execute(db.select(Game).filter_by(id=game_uuid)).scalar_one_or_none()
    if not game:
        return {"error": "Game not found."}, 404

    return {"game": {"id": game.id, 
                     "bonus_per_round": game.bonus_per_round,
                     "start_value": game.start_value,
                     "number_of_operations": game.number_of_operations,
                     "number_of_players": len(game.players)}}, 200
