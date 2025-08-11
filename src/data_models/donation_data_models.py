from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Donation(BaseModel):
    """
    Data model for a donation.
    """

    donation_id: str
    email_address: Optional[str] = ""
    amount: float
    timestamp: datetime
    first_name: str
    last_name: str
    status: bool = False
