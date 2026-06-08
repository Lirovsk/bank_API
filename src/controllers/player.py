from ..app.models import Player, Game
from ..app import db
from ..Services import Utils, PlayerCRUD

from flask import Blueprint, request


app = Blueprint("player", __name__, url_prefix="/players")



#==================== routes ====================#
@app.route("/create", methods=["POST"])
@app.route("/create/<game_uuid>", methods=["POST"])
def create_player(game_uuid=None):
    data = request.get_json()
    return PlayerCRUD.create_player(data, game_uuid)


@app.route("/create/banker/<game_uuid>", methods=["POST"])
def create_banker(game_uuid):
    data = request.get_json()
    return PlayerCRUD.create_banker(data, game_uuid)


@app.route("/delete", methods=["DELETE"])
@app.route("/delete/<int:player_id>", methods=["DELETE"])
def delete_player(player_id=None):
    data = request.get_json(silent=True)
    return PlayerCRUD.delete_player(data, player_id)



@app.route("/update", methods=["PATCH"])
def update_player():
    data = request.get_json()
    return PlayerCRUD.update_player(data)


@app.route("/get/one", methods=["GET"])
@app.route("/get/one/<int:player_id>", methods=["GET"])
def get_player(player_id=None):
    data = request.get_json(silent=True)
    return PlayerCRUD.get_player(data, player_id)


@app.route("/get/all/<game_uuid>", methods=["GET"])
def get_players_by_game(game_uuid):
    return PlayerCRUD.get_players_by_game(game_uuid)
