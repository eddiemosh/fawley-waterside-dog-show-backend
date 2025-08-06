import stripe
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.constants.stripe_price_ids import test_pedigree_price_ids
from src.services.orders import Orders
from src.utils.stripe_utils import generate_line_items

router = APIRouter(prefix="", tags=["Payments"])


class PostPaymentIntent(BaseModel):
    amount: int
    test_mode: bool = False


YOUR_DOMAIN = "https://fawleydogshow.com"

normal_ticket_price_id = ""
pedigree_ticket_price_id = "price_1RsD9ICYSxVmD9YEw0WSgElm"


class PedigreeTickets(BaseModel):
    any_puppy: int = 0
    any_junior: int = 0
    any_gundog: int = 0
    any_utility: int = 0
    any_hound: int = 0
    any_toy: int = 0
    any_working: int = 0
    any_pastoral: int = 0
    any_terrier: int = 0
    any_open: int = 0
    any_veteran: int = 0
    junior_handler: int = 0


class AllDogTickets(BaseModel):
    puppy: int = 0
    prettiest: int = 0
    best_condition: int = 0
    best_rescue: int = 0
    waggiest_tale: int = 0
    childs_best_friend: int = 0
    fancy_dress: int = 0
    handsome: int = 0
    fluffiest: int = 0
    scruffiest: int = 0
    smooth: int = 0
    looks_like_owner: int = 0
    obedience: int = 0
    golden_oldie: int = 0


@router.post("/create-payment-intent", tags=["Payments"])
def submit_payment(
        first_name: str,
        last_name: str,
        email_address: str,
        doggie_info: dict,
        pedigree_tickets: PedigreeTickets,
        all_dog_tickets: AllDogTickets,
):
    print(f"Creating order with name: {first_name}, {last_name}")
    order = Orders.create_order(
        first_name=first_name,
        last_name=last_name,
        email_address=email_address,
        doggie_info=doggie_info,
        pedigree_tickets=pedigree_tickets,
        all_dog_tickets=all_dog_tickets,
    )
    print(f"Created order with result {order}")
    try:
        line_items = []
        # line_items += generate_line_items(ticket_data=pedigree_tickets, price_ids=pedigree_price_ids)
        # line_items += generate_line_items(ticket_data=all_dog_tickets, price_ids=all_dog_price_ids)
        line_items += generate_line_items(ticket_data=pedigree_tickets, price_ids=test_pedigree_price_ids)
        line_items += generate_line_items(ticket_data=all_dog_tickets, price_ids=test_pedigree_price_ids)

        if not line_items:
            raise HTTPException(status_code=400, detail="No tickets selected.")

        checkout_session = stripe.checkout.Session.create(
            line_items=line_items,
            mode="payment",
            success_url=YOUR_DOMAIN + f"/success-order?orderId={order.order_id}",
            cancel_url=YOUR_DOMAIN + f"/failure-order?orderId={order.order_id}",
            automatic_tax={"enabled": True},
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "order_id": order.order_id,
        "url": checkout_session.url,
    }


