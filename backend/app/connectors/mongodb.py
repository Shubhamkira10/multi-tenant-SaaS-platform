from pymongo import MongoClient


class MongoDBConnector:
    def __init__(self, database_url: str):
        self.client = MongoClient(database_url)

    def database(self, name: str):
        return self.client[name]