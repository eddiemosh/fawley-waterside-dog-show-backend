import uuid

from src.data_models.order_data_models import Order, DoggieInfo
from src.routers.payment_router import AllDogTickets, PedigreeTickets
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
    ):
        """
        Create an order in the database
        :return: the order id
        """
        try:
            order_id = str(uuid.uuid4())
            list_of_dogs = []
            for info in doggie_info:
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
            )
            result = self.database_service.create_order(order=order)
            if not result:
                raise Exception(f"False result when attempting to create order in db")
        except Exception as ex:
            print(f"Exception {ex} when attempting to create order")

    def update_order_status(self, order_id: str, status: bool):
        result = self.database_service.update_order(order_id=order_id, status=status)
        return Order(**result)

    def get_order(self, order_id: str):
        result = self.database_service.get_order(order_id=order_id)
        return Order(**result)
