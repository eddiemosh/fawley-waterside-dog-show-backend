from fastapi import APIRouter, HTTPException

from src.services.orders import OrderService

router = APIRouter(prefix="order", tags=["Orders"])


order_service = OrderService()


@router.get("/")
def get_order(order_id: str):
    order = order_service.get_order(order_id=order_id)
    if order:
        return order
    raise HTTPException(status_code=404, detail="Order Not Found")