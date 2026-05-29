from ..app.models import Player, Game
from ..app import db

from flask import Blueprint, request


app = Blueprint("player", __name__, url_prefix="/players")



#==================== routes ====================#
@app.route("/create", methods=["POST"])
@app.route("/create/<game_uuid>", methods=["POST"])
def create_player(game_uuid=None):
    data = request.get_json()
    
    if not game_uuid:
        game_uuid_body = data.get("game_uuid", None)
    else:
        game_uuid_body = game_uuid
    
    name = data.get("name", None)
    if not name:
        return {"error": "name is required."}, 400
    
    game = db.session.execute(db.select(Game).filter_by(id=game_uuid_body)).scalar_one_or_none()
    if not game:
        return {"error": "Game not found"}, 404
    
    balance = game.start_value
    
    # Bind through the ORM relationship so player/game linkage stays consistent
    # for future transaction validation by game_uuid.
    new_player = Player(name=name, balance=balance, game=game)
    try:
        db.session.add(new_player)
        db.session.commit()
        
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500
    
    return {"message": "Player created successfully.", "player_id": new_player.id}, 201


@app.route("/delete", methods=["DELETE"])
@app.route("/delete/<player_id>", methods=["DELETE"])
def delete_player(player_id=None):
    if not player_id:
        data = request.get_json()
        player_id_body = data.get("player_id", None)
        if not player_id_body:
            return {"error": "player_id is required."}, 400
    else:
        player_id_body = player_id
    
    player_to_delete = db.session.execute(db.select(Player).filter_by(id=player_id_body)).scalar_one_or_none()
    if not player_to_delete:
        return {"error": "Player not found."}, 404
    
    try:
        db.session.delete(player_to_delete)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500
    
    return {"message": "Player deleted successfully."}, 200


@app.route("/update", methods=["PATCH"])
def update_player():
    data = request.get_json()
    
    player_id = data.get("player_id", None)
    if not player_id:
        return {"error": "player_id is required."}, 400
    
    player = db.session.execute(db.select(Player).filter_by(id=player_id)).scalar_one_or_none()
    if not player:
        return {"error": "Player not found."}, 404
    
    for info in data:
        if hasattr(player, info):
            if info in ("id", "balance", "game","game_uuid", "transactions_made", "transactions_received", "player_id"):
                continue
            
            setattr(player, info, data[info])
            
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500
    
    return {"message": "Player updated successfully."}, 200


@app.route("/get/one", methods=["GET"])
@app.route("/get/one/<player_id>", methods=["GET"])
def get_player(player_id=None):
    if not player_id:
        data = request.get_json()
        player_id_body = data.get("player_id", None)
        if not player_id_body:
            return {"error": "player_id is required."}, 400
    else:
        player_id_body = player_id
    
    player = db.session.execute(db.select(Player).filter_by(id=player_id_body)).scalar_one_or_none()
    if not player:
        return {"error": "Player not found."}, 404
    
    return {"player": {"id": player.id,
                      "name": player.name,
                      "balance": player.balance,
                      "game_uuid": player.game_uuid,
                      "transactions_made": len(player.transactions_made),
                      "transactions_received": len(player.transactions_received)}}, 200
    
    
@app.route("/get/all/<game_uuid>", methods=["GET"])
def get_players_by_game(game_uuid):
    players = db.session.execute(db.select(Player).filter_by(game_uuid=game_uuid)).scalars().all()
    return {"players": [{"id": player.id,
                        "name": player.name,
                        "balance": player.balance,
                        "game_uuid": player.game_uuid,
                        "transactions_made": len(player.transactions_made),
                        "transactions_received": len(player.transactions_received)} for player in players]}, 200
