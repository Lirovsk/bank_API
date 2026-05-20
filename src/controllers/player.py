from ..models import Player
from .session_and_engine import EscopedEngines
from ..app import db_engines

from flask import Blueprint, request, g

from sqlalchemy.orm import sessionmaker

app = Blueprint("player", __name__, url_prefix="/player")


@app.before_request
def preparing_session():
    game_uuid = request.view_args.get("game_id", None)
    
    if game_uuid is not None:
        engine = db_engines.get_engine(EscopedEngines.create_url(game_uuid))
        Session = sessionmaker(bind=engine)
        
        g.db_session = Session()
        return
    

@app.teardown_request
def remove_session(response):
    db_session = getattr(g, "db_session", None)
    
    if db_session is not None:
        db_session.close()
    
    return response


@app.route("/create/<string:game_id>", methods=["POST"])
def create_player(game_id):
    # Implementation for creating a player
    pass


@app.route("/delete/<string:game_id>/<string:player_id>", methods=["DELETE"])
def delete_player(game_id, player_id):
    # Implementation for deleting a player
    pass


@app.route("/list/<string:game_id>", methods=["GET"])
def list_players(game_id):
    # Implementation for listing players
    pass


@app.route("/update_balance/<string:game_id>/<string:player_id>", methods=["POST"])
def update_player_balance(game_id, player_id):
    # Implementation for updating a player's balance
    pass


@app.route("/set_banker/<string:game_id>/<string:player_id>", methods=["POST"])
def set_player_banker(game_id, player_id):
    # Implementation for setting a player as banker
    pass


@app.route("/update_name/<string:game_id>/<string:player_id>", methods=["POST"])
def update_player_name(game_id, player_id):
    # Implementation for updating a player's name
    pass
