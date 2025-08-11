from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class FeedbackRatings(BaseModel):
    """
    Data model for feedback ratings.
    """

    activities: Optional[int] = None
    value_for_money: Optional[int] = None
    atmosphere: Optional[int] = None
    food_and_drink: Optional[int] = None
    vendors: Optional[int] = None
    overall_experience: Optional[int] = None


class FeedbackSubmission(BaseModel):
    """
    Data model for feedback submission.
    """

    feedback_id: str
    email_address: str
    message: str
    ratings: FeedbackRatings
    timestamp: datetime
