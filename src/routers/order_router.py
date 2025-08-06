from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from src.services.orders import OrderService

router = APIRouter(prefix="/order", tags=["Orders"])


order_service = OrderService()


@router.get("/")
def get_order(order_id: str):
    try:
        order = order_service.get_order(order_id=order_id)
        if order:
            return order
        raise HTTPException(status_code=404, detail="Order Not Found")
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
        return result
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))