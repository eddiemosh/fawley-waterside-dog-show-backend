import json
import random
import string
import uuid
from datetime import datetime

from pymongo.results import UpdateResult

from src.data_models.order_data_models import DoggieInfo, Order
from src.data_models.tickets_data_models import AllDogTickets, PedigreeTickets
from src.services.database import Database


class OrderService:
    """
    Manage orders
    """

    database_service = Database()

    def create_order(
        self,
        first_name: str,
        last_name: str,
        email_address: str,
        doggie_info: dict,
        pedigree_tickets: dict,
        all_dog_tickets: dict,
        order_status: bool = False,
        amount: str = "TBD",
    ) -> Order:
        """
        Create an order in the database
        :return: the order id
        """
        try:
            order_id = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
            list_of_dogs = []
            for key, info in doggie_info.items():
                list_of_dogs.append(DoggieInfo(**info))

            order = Order(
                order_id=order_id,
                first_name=first_name,
                last_name=last_name,
                email_address=email_address,
                doggie_info=list_of_dogs,
                pedigree_tickets=PedigreeTickets(**pedigree_tickets),
                all_dog_tickets=AllDogTickets(**all_dog_tickets),
                order_status=order_status,
                amount=amount,
            )
            result = self.database_service.create_order(order=order)
            if not result:
                raise Exception(f"False result when attempting to create order in db")
            return order
        except Exception as ex:
            print(f"Exception {ex} when attempting to create order")
            raise ex

    def update_order_status(self, order_id: str, status: bool, date_of_purchase: datetime) -> UpdateResult:
        result = self.database_service.update_order_status(
            order_id=order_id, status=status, date_of_purchase=date_of_purchase
        )
        return result

    def get_order(self, order_id: str):
        result = self.database_service.get_order(order_id=order_id)
        return Order(**result)

    def get_orders(self):
        results = self.database_service.get_orders()
        orders = [Order(**result) for result in results]
        return orders

    def get_orders_by_ticket(self, ticket: str):
        results = self.database_service.get_orders_by_ticket(ticket=ticket)
        orders = [Order(**result) for result in results]
        return orders

    def get_test_mode(self):
        result = self.database_service.get_test_mode()
        return result

    def update_test_mode(self, test_mode: bool):
        result = self.database_service.update_test_mode(test_mode=test_mode)
        return result

    def update_order_amount(self, order_id: str, amount: str):
        result = self.database_service.update_order_amount(order_id=order_id, amount=amount)
        return result

    def delete_order(self, order_id: str):
        result = self.database_service.delete_order(order_id=order_id)
        return result
