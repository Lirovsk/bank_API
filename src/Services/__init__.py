"""
This module will contain the services that will be used by the controllers, the goal here is to separate the business logic from the controllers.
The services will be responsible for handling the business logic of the application, such as creating a new game, creating a new player, etc. 
The controllers will be responsible for handling the HTTP requests and responses, and will call the services to perform the necessary actions.    
"""

"Importing the engine from the app module"
from ..app import db

"Importing from this module"
from .utils import Utils
from .game import GameServices, GameCRUD
from .player import PlayerServices, PlayerCRUD
from .transaction import TransactionServices, TransactionCRUD
