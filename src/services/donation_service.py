from datetime import timezone, datetime
from typing import Optional

import stripe
from pydantic import ValidationError

from src.data_models.donation_data_models import Donation
from src.repositories.donations_repository import DonationsRepository
from src.utils.record_id import generate_id
from src.utils.stripe_utils import get_stripe_key


class DonationService:
    """
    Manage donations
    """

    donation_repository = DonationsRepository()
    stripe.api_version = "2025-03-31.basil"
    stripe.api_key = get_stripe_key()

    def get_donations(self) -> list[Donation]:
        try:
            results = self.donation_repository.get_all_donations()
            donations = [Donation(**result) for result in results]
        except ValidationError as ve:
            raise Exception(f"Validation error while processing donations: {str(repr(ve.errors()))}")
        except Exception as ex:
            raise Exception(f"Failed to fetch feedback submissions: {str(ex)}")
        return donations

    def create_donation(
        self, first_name: str, last_name: str, amount: float, email_address: Optional[str] = ""
    ) -> Donation:
        donation = Donation(
            first_name=first_name,
            last_name=last_name,
            email_address=email_address,
            amount=amount,
            timestamp=datetime.now(tz=timezone.utc),
            donation_id=generate_id(),
        )
        result = self.donation_repository.create_donation(donation=donation)
        if not result:
            raise Exception("Failed to create donation in the database")

        print(f"Donation {donation.model_dump()} created with ID: {donation.donation_id}")
        return donation