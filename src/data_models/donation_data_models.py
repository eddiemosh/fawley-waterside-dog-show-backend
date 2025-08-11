from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Donation(BaseModel):
    """
    Data model for a donation.
    """

    donation_id: str
    email_address: Optional[str] = None
    amount: float
    timestamp: datetime
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    status: bool = False
