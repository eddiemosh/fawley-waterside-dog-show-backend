from http import HTTPStatus
from typing import Optional

import stripe
from fastapi import APIRouter, HTTPException

from src.constants.stripe_product_ids import live_donation_product_id, test_donation_product_id
from src.repositories.test_repository import TestRepository
from src.services.donation_service import DonationService
from src.services.email_service import EmailService
from src.utils.stripe_utils import DOGSHOW_DOMAIN, get_stripe_key

router = APIRouter(prefix="/donation", tags=["Donations"])

stripe.api_version = "2025-03-31.basil"
donation_service = DonationService()


@router.post("/create", status_code=HTTPStatus.CREATED)
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
        if TestRepository().get_test_mode():
            donation_product_id = test_donation_product_id
        else:
            donation_product_id = live_donation_product_id
        stripe.api_key = get_stripe_key()

        session = stripe.checkout.Session.create(
            success_url=DOGSHOW_DOMAIN + f"/donation-success?donationId={donation.donation_id}",
            cancel_url=DOGSHOW_DOMAIN + f"/donation-failure?donationId={donation.donation_id}",
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

@router.get("", status_code=HTTPStatus.OK)
def get_donation(donation_id: Optional[str] = None):
    """
    Get a donation by ID.
    :param donation_id: The ID of the donation to retrieve. If not provided, returns all donations.
    :return: The donation details.
    """
    try:
        donations = donation_service.get_donations(donation_id=donation_id)
        return donations
    except Exception as ex:
        print("Error fetching donations:", str(ex))
        raise HTTPException(status_code=500, detail=str(ex))


@router.delete("/delete", status_code=HTTPStatus.ACCEPTED)
def delete_donation(donation_id: str):
    """
    Delete a donation by ID.
    :param donation_id: The ID of the donation to delete.
    :return: A message indicating the donation was deleted successfully.
    """
    try:
        result = donation_service.delete_donation(donation_id=donation_id)
        if result:
            return {"message": f"Donation with ID {donation_id} deleted successfully."}
        else:
            raise HTTPException(status_code=404, detail=f"Donation with ID {donation_id} not found.")
    except Exception as ex:
        print("Error deleting donation:", str(ex))
        raise HTTPException(status_code=500, detail=str(ex))