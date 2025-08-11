from datetime import datetime, timezone
from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, HTTPException

from src.services.email_service import EmailService
from src.services.order_service import OrderService

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
            return orders
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@router.post("/create", status_code=HTTPStatus.CREATED)
def create_order(
    first_name: str,
    last_name: str,
    doggie_info: dict,
    pedigree_tickets: dict,
    all_dog_tickets: dict,
    order_status: bool = False,
    email_address: str = "",
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
def successful_order(order_id: dict) -> int:
    try:
        order_id_value = order_id.get("order_id")
        if not order_id_value:
            raise Exception("Order ID not provided in request body")
        date_of_purchase = datetime.now(tz=timezone.utc)
        update_result = order_service.update_order_details(
            order_id=order_id_value, status=True, date_of_purchase=date_of_purchase
        )
        if not update_result:
            print("Order was found but not updated as status already True")
        print(f"Successfully updated order {order_id}")

        order = order_service.get_order(order_id=order_id_value)
        purchased_tickets = []
        pedigree_tickets = order.pedigree_tickets.model_dump() if order.pedigree_tickets else {}
        all_dog_tickets = order.all_dog_tickets.model_dump() if order.all_dog_tickets else {}
        combined_tickets = {**pedigree_tickets, **all_dog_tickets}
        for ticket_name, quantity in combined_tickets.items():
            if quantity:
                purchased_tickets.append({ticket_name: quantity})

        if order.email_address:  # Only send email if email address is provided
            print(f"Sending confirmation email to {order.email_address} for order {order.order_id}")
            email_result = EmailService.send_confirmation_email(
                to_email=order.email_address,
                subject="Order Confirmation",
                name=order.first_name,
                order_id=order.order_id,
                tickets=purchased_tickets,
                date_of_purchase=order.date_of_purchase.strftime("%Y-%m-%d %H:%M:%S"),
                amount=order.amount,
            )
            if not email_result:
                raise Exception("Failed to send email")
        return int(HTTPStatus.ACCEPTED)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error performing successful order workflow due to {str(ex)}")


@router.delete("/delete", status_code=HTTPStatus.ACCEPTED)
def delete_order(order_id: dict) -> int:
    try:
        order_id_value = order_id.get("order_id")
        if not order_id_value:
            raise Exception("Order ID not provided in request body")
        result = order_service.orders_repository.delete_order(order_id=order_id_value)
        if not result:
            raise Exception(f"Failed to delete order with id {order_id_value}")
        return int(HTTPStatus.ACCEPTED)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error deleting order due to {str(ex)}")
