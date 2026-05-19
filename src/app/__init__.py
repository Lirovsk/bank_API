import os
from pathlib import Path

import click
from flask import Flask, current_app, Blueprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


# filepath: c:\Users\Arauj\Documents\VScode\python\projetos\flask-project\src\app\__init__.py
@click.command("init-db")
def init_db_command():
    """Create the database tables."""
    
    with current_app.app_context():
        db.create_all()
    click.echo("Initialized the database.")


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="sqlite:///main.db",
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)

    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance and the games folders exists
    if Path(app.instance_path).exists() is False:
        Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    
    games = Path(app.instance_path) / "games"
    
    if games.exists() is False:
        games.mkdir(parents=True, exist_ok=True)


    # command to initialize the database
    app.cli.add_command(init_db_command)
    db.init_app(app)
    
    from ..controllers import create_game
    app.register_blueprint(create_game.app)
    
    return app
