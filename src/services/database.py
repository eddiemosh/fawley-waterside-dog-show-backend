import json
import os
from datetime import datetime
from urllib.parse import quote_plus

from pymongo import MongoClient

from src.services.orders import Order


class Database:
    """
    Database manager (Singleton)
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "_initialized") and self._initialized:
            return
        db_credentials = json.loads(os.environ.get("DB_CREDENTIALS"))
        db_password = db_credentials.get("password")
        connection_string = f"mongodb://dogshow:{quote_plus(db_password)}@dogshow.cluster-c3owqu6m8ncl.eu-north-1.docdb.amazonaws.com:27017/?tls=true&tlsCAFile=global-bundle.pem&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false"
        mongo_client = MongoClient(connection_string)
        db = mongo_client["dogshow"]
        self.orders_collection = db["orders"]
        self.orders_collection.create_index("order_id", unique=True)
        self._initialized = True

        orders = self.get_orders()
        count=0
        for order in orders:
            if order.first_name == "Edward" and order.date_of_purchase is None and len(order.order_id) > 10:
                self.delete_order(order_id=order.order_id)
                count+=1
        print(f"Deleted {count} orders")

    def get_order(self, order_id: str) -> dict:
        result = self.orders_collection.find_one({"order_id": order_id}, {"id": 0})
        return result

    def get_orders(self) -> list:
        results = self.orders_collection.find({}, {"id": 0})
        return list(results)

    def get_orders_by_ticket(self, ticket: str):
        """
        Get all orders by ticket
        :param ticket: the name of the ticket to filter by
        :return: all orders with that ticket present
        """
        pedigree_results = list(
            self.orders_collection.find({f"pedigree_tickets.{ticket}": {"$gt": 0}}, {"id": 0})
        )
        all_dog_results = list(self.orders_collection.find({f"all_dog_tickets.{ticket}": {"$gt": 0}}, {"id": 0}))
        return pedigree_results + all_dog_results

    def create_order(self, order: Order) -> bool:
        """
        Create order
        :param order: order details
        :return: true if order was created in db
        """
        result = self.orders_collection.insert_one(order.model_dump(exclude_none=True))
        if result.inserted_id:
            print("Order created with result", result)
            return True
        return False

    def update_order(self, order_id: str, status: bool, date_of_purchase: datetime):
        result = self.orders_collection.update_one({"order_id": order_id}, {"$set": {"order_status": status, "date_of_purchase": date_of_purchase}})
        if result.modified_count:
            return result
        if not result.matched_count:
            raise Exception("Order not found")
        return False

    def delete_order(self, order_id: str) -> bool:
        result = self.orders_collection.delete_one({"order_id": order_id})
        if result.deleted_count:
            print(f"Order {order_id} deleted successfully")
            return True
        print(f"Order {order_id} not found or already deleted")
        return False
