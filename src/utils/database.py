import json
import os
from urllib.parse import quote_plus

from pymongo import MongoClient


class Database:
    """
    Database connection manager (Singleton)
    """

    _instance = None
    _client = None
    _db = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "_initialized") and self._initialized:
            return
        db_credentials = json.loads(os.environ.get("DB_CREDENTIALS"))
        db_password = db_credentials.get("password")
        connection_string = (
            f"mongodb://dogshow:{quote_plus(db_password)}"
            f"@dogshow.cluster-c3owqu6m8ncl.eu-north-1.docdb.amazonaws.com:27017/?tls=true"
            f"&tlsCAFile=global-bundle.pem&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false"
        )
        self._client = MongoClient(connection_string)
        self._db = self._client["dogshow"]
        self._initialized = True

    def get_db(self):
        return self._db

    def get_collection(self, name: str):
        return self._db[name]
