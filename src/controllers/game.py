from ..models import Game
from ..app import db
from ..Services import GameCRUD

from flask import Blueprint, request
from flask_jwt_extended import jwt_required


app = Blueprint("game", __name__, url_prefix="/games")



#==================== routes ====================#
@app.route("/create", methods=["POST"])
@jwt_required()
def create_game():
    data = request.get_json()
    return GameCRUD.create_game(data)


@app.route("/delete", methods=["DELETE"])
@jwt_required()
def delete_game():
    data = request.get_json()
    return GameCRUD.delete_game(data)


@app.route("/update", methods=["PATCH"])
@jwt_required()
def update_game():
    data = request.get_json()
    return GameCRUD.update_game(data)


@app.route("/get/<string:game_uuid>", methods=["GET"])
@jwt_required()
def get_game(game_uuid):
    return GameCRUD.get_game(game_uuid)
