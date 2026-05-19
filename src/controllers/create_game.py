from flask import Blueprint, request, current_app
from ..app import db
from ..models import Game

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from ..models import Player, Transaction

app = Blueprint("game", __name__, url_prefix="/game")


# ======================== functions ========================
def create_game_tables(game_uuid: str):
    # turn the following lines into a function that creates the engine
    game_path = Path(current_app.instance_path) / "games" / f"{game_uuid}.db"
    engine = create_engine(f"sqlite:///{game_path}")

    try:
        Player.__table__.create(bind=engine, checkfirst=True)
        Transaction.__table__.create(bind=engine, checkfirst=True)
    except Exception as e:
        return {"error": f"Error creating tables: {str(e)}",
                "status": False}
    
    return {"message": "Tables created successfully", "status": True}


# ======================== endpoints ========================
@app.route("/create", methods=["POST"])
def create_game():
    data = request.get_json()

    game = Game(
        bonus_per_round=data.get("bonus_per_round"),
        rules_from=data.get("rules_from", None),
    )

    db.session.add(game)
    db.session.commit()
    
    response = create_game_tables(game.id)
    if response["status"] is False:
        db.session.delete(game)
        db.session.commit()
        return {"error": response["error"]}, 500

    return {"game_uuid": str(game.id)}, 201


@app.route("/delete/<string:game_id>", methods=["DELETE"])
def delete_game(game_id):
    game = Game.query.get(game_id)

    if not game:
        return {"error": "Game not found"}, 404

    db.session.delete(game)
    db.session.commit()

    return {"message": "Game deleted successfully"}, 200


@app.route("/list", methods=["GET"])
def list_games():
    games = Game.query.all()

    return {"games": [game.__repr__() for game in games]}, 200
