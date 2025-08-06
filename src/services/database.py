import os
from urllib.parse import quote_plus

import json
from pymongo import MongoClient

from src.services.orders import Order


class Database:
    """
    Database manager
    """

    def __init__(self):
        db_credentials = json.loads(os.environ.get("DB_CREDENTIALS"))
        db_password = db_credentials.get("password")
        print(f"password shortened is type {type(db_password)}")
        print(f"and content {db_password}")
        connection_string = f"mongodb://dogshow:{quote_plus(db_password)}@dogshow.cluster-c3owqu6m8ncl.eu-north-1.docdb.amazonaws.com:27017/?tls=true&tlsCAFile=global-bundle.pem&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false"
        mongo_client = MongoClient(connection_string)
        db = mongo_client["dogshow"]
        self.orders_collection = db["orders"]
        self.orders_collection.create_index("order_id")

    def get_order(self, order_id: str) -> dict:
        result = self.orders_collection.find_one({"order_id": order_id}, {"id": 0})
        return result

    def create_order(self, order: Order) -> bool:
        """
        Create order
        :param order: order details
        :return: true if order was created in db
        """
        result = self.orders_collection.insert_one(order.model_dump())
        if result.inserted_id:
            print("Order created with result", result)
            return True
        return False

    def update_order(self, order_id: str, status: bool):
        result = self.orders_collection.update_one({"order_id": order_id}, {"order_status": status})
        if result.modified_count:
            return result
        if result.matched_count:
            raise Exception("Order not found")
        return False
