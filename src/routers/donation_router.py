from http import HTTPStatus

import stripe
from fastapi import APIRouter, HTTPException

from src.constants.stripe_product_ids import donation_product_id
from src.services.donation_service import DonationService
from src.services.email_service import EmailService
from src.utils.stripe_utils import DOGSHOW_DOMAIN, get_stripe_key

router = APIRouter(prefix="/donation", tags=["Donations"])

stripe.api_version = "2025-03-31.basil"
stripe.api_key = get_stripe_key()
donation_service = DonationService()


@router.post("/donation", status_code=HTTPStatus.CREATED)
def record_donation(payload: dict):
    """
    Record a donation.
    :param payload: Payload containing donation details.
    :return: A message indicating the donation was recorded successfully.
    """
    try:
        donation = donation_service.create_donation(
            first_name=payload.get("first_name"),
            last_name=payload.get("last_name"),
            email_address=payload.get("email_address", ""),
            amount=payload.get("amount"),
        )
        session = stripe.checkout.Session.create(
            success_url=DOGSHOW_DOMAIN + f"/donation-success?donation_id={donation.donation_id}",
            cancel_url=DOGSHOW_DOMAIN + f"/donation-failure?donation_id={donation.donation_id}",
            line_items=[
                {
                    "price_data": {
                        "currency": "gbp",
                        "product": donation_product_id,
                        "unit_amount": int(donation.amount * 100),
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
        )
        if donation.email_address:
            EmailService.send_donation_confirmation_email(
                to_email=donation.email_address,
                name=f"{donation.first_name}",
                donation_id=donation.donation_id,
                amount=str(donation.amount),
                date_of_donation=donation.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            )
        return {"donation_id": donation.donation_id, "checkout_url": session.url}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
