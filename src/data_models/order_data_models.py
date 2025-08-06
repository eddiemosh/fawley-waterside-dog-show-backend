from typing import Optional

from pydantic import BaseModel

from src.data_models.tickets_data_models import PedigreeTickets, AllDogTickets


class PostPaymentIntent(BaseModel):
    amount: int
    test_mode: bool = False


class DoggieInfo(BaseModel):
    name: str
    date_of_birth: str
    sex: str


class Order(BaseModel):
    order_id: str
    first_name: str
    last_name: str
    email_address: str
    doggie_info: list[DoggieInfo]
    pedigree_tickets: Optional[PedigreeTickets] = None
    all_dog_tickets: Optional[AllDogTickets] = None
    order_status: bool = False
