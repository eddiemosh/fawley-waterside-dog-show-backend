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
def send_promotion(promotion_type: PromotionType, name: str, email_address: str):
    if not promotion_type == PromotionType.FEEDBACK:
        raise HTTPException(status_code=400, detail="Unsupported promotion type")
    try:
        email_service = EmailService()
        order_service = OrderService()
        # orders = order_service.get_orders()
        orders = [
            Order(
                first_name="ed",
                last_name="hardy",
                doggie_info=[DoggieInfo(name="dog1", date_of_birth="2025-12", sex="male")],
                email_address="hardyedward18@gmail.com",
                order_id="test_order_id",
                amount="12.00",
                pedigree_tickets=PedigreeTickets(),
                all_dog_tickets=AllDogTickets(),
            )
        ]  # Mocking an order for testing purposes)]
        for order in orders:
            if order.email_address:
                email_service.send_feedback_email(name=order.first_name, to_email=order.email_address)
        return {"message": "Feedback promotion emails sent successfully"}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
