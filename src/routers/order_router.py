import stripe
from fastapi import APIRouter, HTTPException

from src.constants.stripe_price_ids import test_pedigree_price_ids, test_all_dog_price_ids
from src.services.orders import OrderService
from src.utils.stripe_utils import generate_line_items

router = APIRouter(prefix="order", tags=["Orders"])


order_service = OrderService()


@router.get("/")
def get_order(order_id: str):
    order = order_service.get_order(order_id=order_id)
    if order:
        return order
    raise HTTPException(status_code=404, detail="Order Not Found")