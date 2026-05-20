from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from flask import current_app

from pathlib import Path


class EscopedEngines():
    
    def __init__(self):
        self.engines = {}
        
        
    def get_engine(self, db_url):
        engine = self.engines.get(db_url, None)
        
        if engine is None:
            self.engines[db_url] = create_engine(db_url)
        
        return self.engines[db_url]
    
    
    @staticmethod
    def create_url(uuid):
        game_path = Path(current_app.instance_path) / "games" / f"{uuid}.db"
        
        return f"sqlite:///{game_path}"