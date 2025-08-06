from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, HTTPException

from src.services.email import EmailService
from src.services.orders import OrderService

router = APIRouter(prefix="/order", tags=["Orders"])


order_service = OrderService()


@router.get("/")
def get_order(order_id: Optional[str] = None):
    try:
        if order_id:
            order = order_service.get_order(order_id=order_id)
            if order:
                return order
            raise HTTPException(status_code=404, detail="Order Not Found")
        else:
            orders = order_service.get_orders()
            if not orders:
                raise Exception("Failure getting all orders")
            return orders
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@router.post("/create", status_code=HTTPStatus.CREATED)
def create_order(
    first_name: str,
    last_name: str,
    email_address: str,
    doggie_info: dict,
    pedigree_tickets: dict,
    all_dog_tickets: dict,
    order_status: bool = False,
):
    try:
        result = order_service.create_order(
            first_name=first_name,
            last_name=last_name,
            email_address=email_address,
            doggie_info=doggie_info,
            pedigree_tickets=pedigree_tickets,
            all_dog_tickets=all_dog_tickets,
            order_status=order_status,
        )
        return {"message": f"Order created with id {result.order_id}"}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@router.put("/success", status_code=HTTPStatus.ACCEPTED)
def successful_order(order_id: str) -> int:
    try:
        order = order_service.update_order_status(order_id=order_id, status=True)
        if not order:
            raise Exception("Error updating order")
        print(f"Successfully updated order {order_id}")

        email_result = EmailService.send_confirmation_email(
            to_email=order.email_address, subject="Order Confirmation", name=order.first_name, order_id=order.order_id
        )
        if not email_result:
            raise Exception(f"Failed to send email")

        return int(HTTPStatus.ACCEPTED)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error performing successful order workflow due to {str(ex)}")

