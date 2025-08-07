import os
from typing import Optional

import stripe
from fastapi import APIRouter, HTTPException

from src.constants.stripe_price_ids import test_all_dog_price_ids, test_pedigree_price_ids
from src.services.orders import OrderService
from src.utils.stripe_utils import generate_line_items

router = APIRouter(prefix="/payment", tags=["Payments"])

YOUR_DOMAIN = "https://fawleydogshow.com"

order_service = OrderService()

secret_key = os.getenv("STRIPE_SECRET_TEST_KEY")
if not secret_key:
    raise ValueError(f"Stripe key not loaded!")

stripe.api_version = "2025-03-31.basil"
stripe.api_key = secret_key


@router.post("/create-payment-intent", tags=["Payments"])
def submit_payment(
    first_name: str,
    last_name: str,
    doggie_info: dict,
    pedigree_tickets: dict,
    all_dog_tickets: dict,
    email_address: str = "",
):
    try:
        print(f"Creating order with name: {first_name}, {last_name}")
        order = order_service.create_order(
            first_name=first_name,
            last_name=last_name,
            email_address=email_address,
            doggie_info=doggie_info,
            pedigree_tickets=pedigree_tickets,
            all_dog_tickets=all_dog_tickets,
        )
        print(f"Created order with result {order}")
        line_items = []
        # line_items += generate_line_items(ticket_data=pedigree_tickets, price_ids=pedigree_price_ids)
        # line_items += generate_line_items(ticket_data=all_dog_tickets, price_ids=all_dog_price_ids)
        line_items += generate_line_items(ticket_data=order.pedigree_tickets, price_ids=test_pedigree_price_ids)
        line_items += generate_line_items(ticket_data=order.all_dog_tickets, price_ids=test_all_dog_price_ids)
        print("line items:", line_items)
        if not line_items:
            raise HTTPException(status_code=400, detail="No tickets selected.")

        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=line_items,
                mode="payment",
                success_url=YOUR_DOMAIN + f"/order-success?orderId={order.order_id}",
                cancel_url=YOUR_DOMAIN + f"/order-failure?orderId={order.order_id}",
                automatic_tax={"enabled": True},
            )
        except Exception as ex:
            print(
                f"Stripe checkout session creation failed due to {str(ex)} with line items {line_items} and order {order.model_dump()}"
            )
            raise ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "order_id": order.order_id,
        "url": checkout_session.url,
    }
