from datetime import datetime, timezone
from enum import Enum
from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from src.data_models.order_data_models import Order, DoggieInfo
from src.data_models.tickets_data_models import PedigreeTickets, AllDogTickets
from src.services.email_service import EmailService
from src.services.order_service import OrderService

router = APIRouter(prefix="/promotion", tags=["Promotions"])


class PromotionType(str, Enum):
    FEEDBACK = "feedback"
    FEEDBACK_REMINDER = "feedback_reminder"


@router.post("", status_code=HTTPStatus.OK)
def send_promotion(promotion_type: PromotionType):
    if promotion_type not in [PromotionType.FEEDBACK, PromotionType.FEEDBACK_REMINDER]:
        raise HTTPException(status_code=400, detail="Unsupported promotion type")
    try:
        email_service = EmailService()
        # order_service = OrderService()
        # orders = order_service.get_orders()
        orders = [
            Order(
                order_id="12345",
                first_name="Ed",
                last_name="Hardy",
                email_address="hardyedward18@gmail.com",
                doggie_info=[DoggieInfo(name="Fido", date_of_birth="2020-01-01", sex="Male")],
                pedigree_tickets=PedigreeTickets(any_puppy=1),
                all_dog_tickets=AllDogTickets(
                    prettiest=1,
                ),
                order_status=True,
                amount="20.00",
                date_of_purchase=datetime.now(tz=timezone.utc),
            )
        ]
        ticket_names = {}
        order_names = {}
        for order in orders:
            if order.email_address:
                if order.email_address not in order_names:
                    print("attemtping to add order name")
                    order_names[order.email_address] = order.first_name
                    print("Attempting to combine ticket lists")
                tickets = order.pedigree_tickets.model_dump(exclude_none=True)
                tickets.update(order.all_dog_tickets.model_dump(exclude_none=True))
                for ticket_name, quantity in tickets.items():
                    print(
                        "Processing ticket:", ticket_name, "with quantity", quantity, "for email:", order.email_address
                    )
                    if order.email_address in ticket_names:
                        existing_tickets = ticket_names.get(order.email_address)  # get existing ticket names
                        print(f"existing tickets for {order.email_address}:", existing_tickets)
                        new_tickets = existing_tickets + [
                            ticket_name.replace("_", " ").title()
                        ]  # add the new ticket name
                        print(f"new tickets for {order.email_address}:", new_tickets)
                        ticket_names[order.email_address] = new_tickets  # set the new value
                        print(
                            "Updated ticket names for email:",
                            order.email_address,
                            "to",
                            ticket_names[order.email_address],
                        )
                    else:
                        print("Adding new ticket name for email:", order.email_address)
                        ticket_names[order.email_address] = [ticket_name.replace("_", " ").title()]
        for email, name in order_names.items():
            try:
                print("Sending feedback email to:", email, "with name:", name, "and tickets:", ticket_names.get(email))
                if promotion_type == PromotionType.FEEDBACK:
                    email_service.send_feedback_email(name=name, to_email=email, tickets=ticket_names.get(email))
                elif promotion_type == PromotionType.FEEDBACK_REMINDER:
                    email_service.send_feedback_reminder_email(
                        name=name, to_email=email, tickets=ticket_names.get(email)
                    )
                else:
                    raise HTTPException(status_code=400, detail="Unsupported promotion type")
            except Exception as ex:
                print(f"Failed to send email to {email} due to {str(ex)}")
        return {"message": "Feedback promotion emails sent successfully"}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
