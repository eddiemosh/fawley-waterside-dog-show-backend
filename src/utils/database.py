import json
import os
from urllib.parse import quote_plus

import boto3
import pymongo
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

    def _fetch_credentials_and_connect(self):
        # Fetch credentials at runtime from AWS Secrets Manager
        secret_name = os.environ.get("DB_SECRET_NAME", "rds!cluster-8f6430cc-b042-441d-a711-6e561cfcc798")
        region_name = os.environ.get("AWS_REGION", "eu-north-1")
        session = boto3.session.Session()
        client = session.client(service_name="secretsmanager", region_name=region_name)
        try:
            get_secret_value_response = client.get_secret_value(SecretId=secret_name)
            db_credentials_raw = get_secret_value_response["SecretString"]
        except Exception as e:
            raise RuntimeError(f"Failed to fetch DB credentials from AWS Secrets Manager: {e}")
        db_credentials = json.loads(db_credentials_raw)
        db_password = db_credentials.get("password")
        if not db_password:
            raise RuntimeError("No password found in DB credentials from AWS Secrets Manager")
        connection_string = (
            f"mongodb://dogshow:{quote_plus(db_password)}"
            f"@dogshow.cluster-c3owqu6m8ncl.eu-north-1.docdb.amazonaws.com:27017/?tls=true"
            f"&tlsCAFile=global-bundle.pem&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false"
        )
        self._client = MongoClient(connection_string)
        self._db = self._client["dogshow"]

    def __init__(self):
        if hasattr(self, "_initialized") and self._initialized:
            return
        self._fetch_credentials_and_connect()
        self._initialized = True

    def get_db(self):
        try:
            # Try a simple command to check connection
            self._db.command("ping")
        except (
            pymongo.errors.OperationFailure,
            pymongo.errors.ConfigurationError,
            pymongo.errors.ServerSelectionTimeoutError,
        ):
            self._fetch_credentials_and_connect()
        return self._db

    def get_collection(self, name: str):
        try:
            self._db.command("ping")
        except (
            pymongo.errors.OperationFailure,
            pymongo.errors.ConfigurationError,
            pymongo.errors.ServerSelectionTimeoutError,
        ):
            self._fetch_credentials_and_connect()
        return self._db[name]
