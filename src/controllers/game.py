from ..app.models import Game
from ..app import db
from ..Services import GameCRUD

from flask import Blueprint, request


app = Blueprint("game", __name__, url_prefix="/games")



#==================== routes ====================#
@app.route("/create", methods=["POST"])
def create_game():
    data = request.get_json()
    return GameCRUD.create_game(data)


@app.route("/delete", methods=["DELETE"])
def delete_game():
    data = request.get_json()
    return GameCRUD.delete_game(data)


@app.route("/update", methods=["PATCH"])
def update_game():
    data = request.get_json()
    return GameCRUD.update_game(data)


@app.route("/get/<string:game_uuid>", methods=["GET"])
def get_game(game_uuid):
    return GameCRUD.get_game(game_uuid)
