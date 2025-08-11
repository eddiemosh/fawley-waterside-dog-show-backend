import os
from typing import Optional

from pydantic import BaseModel

from src.repositories.test_repository import TestRepository

DOGSHOW_DOMAIN = "https://fawleydogshow.com"


def generate_line_items(ticket_data: Optional[BaseModel], price_ids: dict) -> list:
    if not ticket_data:
        return []
    line_items = []

    for field_name, quantity in ticket_data.model_dump(exclude_none=True).items():
        price_id = price_ids.get(field_name)
        if not price_id:
            raise ValueError(f"Missing price ID for ticket type: {field_name}")
        line_items.append(
            {
                "price": price_id,
                "quantity": quantity,
            }
        )
    return line_items


def get_stripe_key():
    secret_key = os.getenv("STRIPE_SECRET_KEY")
    test_secret_key = os.getenv("STRIPE_SECRET_TEST_KEY")

    if not secret_key:
        raise ValueError("Stripe key not loaded!")
    if not test_secret_key:
        raise ValueError("Stripe key not loaded!")

    if TestRepository().get_test_mode() is True:
        return test_secret_key
    else:
        return secret_key
