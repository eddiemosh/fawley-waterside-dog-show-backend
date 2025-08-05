import stripe
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
import os

secret_key = os.getenv("STRIPE_SECRET_TEST_KEY")

stripe.api_version = "2025-03-31.basil"
stripe.api_key = secret_key

app = FastAPI(title="Dog Show Backend")

currency = "gbp"
origins = [
    "http://localhost:3000",  # Local frontend (React dev server)
    "https://fawleydogshow.com",  # Your deployed frontend domain
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

YOUR_DOMAIN = "https://fawleydogshow.com"


class PostPaymentIntent(BaseModel):
    amount: int
    test_mode: bool = False


normal_ticket_price_id = ""
pedigree_ticket_price_id = "price_1RsD9ICYSxVmD9YEw0WSgElm"


@app.post("/create-payment-intent", tags=["Payments"])
def submit_payment(num_of_pedigree_tickets: int, num_of_normal_tickets: int):
    line_items = []
    if pedigree_ticket_price_id:
        line_items.append(
            {
                "price": pedigree_ticket_price_id,
                "quantity": num_of_pedigree_tickets,
            }
        )
    if normal_ticket_price_id:
        line_items.append(
            {
                "price": normal_ticket_price_id,
                "quantity": num_of_normal_tickets,
            }
        )
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=line_items,
            mode="payment",
            success_url=YOUR_DOMAIN,
            cancel_url=YOUR_DOMAIN,
            automatic_tax={"enabled": True},
        )
        return {
            "sessionId": checkout_session.id,
            "url": checkout_session.url,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/", tags=["Health"])
def get_health():
    return True


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
