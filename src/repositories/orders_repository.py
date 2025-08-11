from datetime import datetime

from src.data_models.order_data_models import Order
from src.utils.database import Database


class OrdersRepository:
    def __init__(self):
        self.collection = Database().get_collection("orders")
        try:
            self.collection.create_index("order_id", unique=True)
        except Exception as ex:
            print(f"Error creating index on 'order_id': {ex}")

    def create_order(self, order: Order):
        return self.collection.insert_one(order.model_dump())

    def get_order(self, order_id: str):
        return self.collection.find_one({"order_id": order_id})

    def get_all_orders(self):
        return list(self.collection.find())

    def get_orders_by_ticket(self, ticket: str):
        return list(
            self.collection.find(
                {"$or": [{f"pedigree_tickets.{ticket}": {"$gt": 0}}, {f"all_dog_tickets.{ticket}": {"$gt": 0}}]}
            )
        )

    def delete_order(self, order_id: str):
        return self.collection.delete_one({"order_id": order_id})

    def update_order_details(self, order_id: str, status: bool, date_of_purchase: datetime):
        return self.collection.update_one(
            {"order_id": order_id}, {"$set": {"status": status, "date_of_purchase": date_of_purchase}}
        )

    def update_order_amount(self, order_id: str, amount: str):
        return self.collection.update_one({"order_id": order_id}, {"$set": {"amount": amount}})
