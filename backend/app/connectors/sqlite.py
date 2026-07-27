from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from app.connectors.base import BaseConnector


class SQLiteConnector(BaseConnector):
    def __init__(self, database_url: str):
        self.database_url = database_url

    def create_engine(self) -> Engine:
        return create_engine(
            self.database_url,
            echo=False,
            future=True,
        )