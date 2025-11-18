import os

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import urllib.parse

from src.utils.database import Database

uri = f"mongodb+srv://hardyedward18_db_user:{os.getenv('ATLAS_DATABASE_PASSWORD')}@fawley-dogshow.0koebfr.mongodb.net/?retryWrites=true&w=majority"
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