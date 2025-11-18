import json
import os

import boto3
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from src.utils.database import Database

secret_name = os.environ.get("ATLAS_DB_NAME", "dogshow/atlas_mongodb")
region_name = os.environ.get("AWS_REGION", "eu-north-1")
session = boto3.session.Session()
client = session.client(service_name="secretsmanager", region_name=region_name)
try:
    get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    db_credentials_raw = get_secret_value_response["SecretString"]
except Exception as e:
    raise RuntimeError(f"Failed to fetch DB credentials from AWS Secrets Manager: {e}")
db_credentials = json.loads(db_credentials_raw)
db_username = None
db_password = None
for key, value in db_credentials.items():
    db_username = key
    db_password = value

if not db_password:
    raise RuntimeError("No password found in DB credentials from AWS Secrets Manager")

if not db_username:
    raise RuntimeError("No username found in DB credentials from AWS Secrets Manager")
uri = f"mongodb+srv://{db_username}:{db_password}@fawley-dogshow.0koebfr.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))

try:
    client.collection_names()
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
    original_database = Database().get_db()
    new_database = client.dogshow
    collections = original_database.list_collection_names()

    for collection in collections:
        print(f"Collection: {collection}")
        original_collection_object = original_database.get_collection(collection)
        new_collection_object = new_database[collection]
        documents = original_collection_object.find()
        for document in documents:
            print("Document ID", document.get("_id"))
            new_collection_object.insert_one(document)
except Exception as e:
    print(e)