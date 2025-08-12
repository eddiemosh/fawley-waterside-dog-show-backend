from enum import Enum
from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from src.data_models.order_data_models import DoggieInfo, Order
from src.data_models.tickets_data_models import AllDogTickets, PedigreeTickets
from src.services.email_service import EmailService
from src.services.order_service import OrderService

router = APIRouter(prefix="/promotion", tags=["Promotions"])


class PromotionType(str, Enum):
    FEEDBACK = "feedback"


@router.post("", status_code=HTTPStatus.OK)
def send_promotion(promotion_type: PromotionType):
    if not promotion_type == PromotionType.FEEDBACK:
        raise HTTPException(status_code=400, detail="Unsupported promotion type")
    try:
        email_service = EmailService()
        # order_service = OrderService()
        # orders = order_service.get_orders()
        orders = [
            Order(
                first_name="ed",
                last_name="hardy",
                doggie_info=[DoggieInfo(name="dog1", date_of_birth="2025-12", sex="male")],
                email_address="hardyedward18@gmail.com",
                order_id="test_order_id",
                amount="12.00",
                pedigree_tickets=PedigreeTickets(any_puppy=1, any_junior=1),
                all_dog_tickets=AllDogTickets(childs_best_friend=1, best_rescue=1),
            ),
            Order(
                first_name="john",
                last_name="doe",
                doggie_info=[DoggieInfo(name="dog1", date_of_birth="2025-12", sex="male")],
                email_address="hardyedward18@gmail.com",
                order_id="test_order_id_2",
                amount="12.00",
                pedigree_tickets=PedigreeTickets(any_toy=1, any_pastoral=1),
                all_dog_tickets=AllDogTickets(puppy=3, best_condition=1),
            ),
            Order(
                first_name="jane",
                last_name="doe",
                doggie_info=[DoggieInfo(name="dog1", date_of_birth="2025-12", sex="male")],
                email_address="hardyedward18@gmail.com",
                order_id="test_order_id_3",
                amount="12.00",
                pedigree_tickets=PedigreeTickets(any_working=2, any_utility=1),
                all_dog_tickets=AllDogTickets(prettiest=1, scruffiest=2),
            ),
        ]  # Mocking an order for testing purposes)]

        ticket_names = {"email": ["tickets"]}
        order_names = {"email": "first_name"}
        for order in orders:
            if order.email_address:
                if order.email_address not in order_names:
                    order_names[order.email_address] = order.first_name
                tickets = order.pedigree_tickets.model_dump(exclude_none=True)
                tickets.update(order.all_dog_tickets.model_dump(exclude_none=True))
                for ticket_name, quantity in tickets.items():
                    if order.email_address in ticket_names:
                        existing_tickets = ticket_names.get(order.email_address)  # get existing ticket names
                        new_tickets = (
                            existing_tickets + ticket_name.replace("_", " ").title()
                        )  # add the new ticket name
                        ticket_names[order.email_address] = new_tickets  # set the new value
                    else:
                        ticket_names[order.email_address] = [ticket_name.replace("_", " ").title()]
        for email, name in order_names.items():
            email_service.send_feedback_email(name=name, to_email=email, tickets=ticket_names.get(email))
        return {"message": "Feedback promotion emails sent successfully"}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
