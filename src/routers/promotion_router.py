from enum import Enum
from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from src.repositories.test_repository import TestRepository
from src.services.email_service import EmailService

router = APIRouter(prefix="/promotion", tags=["Promotions"])


class PromotionType(str, Enum):
    FEEDBACK = "feedback"


@router.post("", status_code=HTTPStatus.OK)
def send_promotion(promotion_type: PromotionType, name: str, email_address: str):
    if not promotion_type == PromotionType.FEEDBACK:
        raise HTTPException(status_code=400, detail="Unsupported promotion type")
    try:
        email_service = EmailService()
        email_service.send_feedback_email(name=name, to_email=email_address)
        return {"message": "Feedback promotion email sent successfully"}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@router.get("", status_code=HTTPStatus.OK)
def get_test_mode():
    try:
        test_repository = TestRepository()
        test_mode = test_repository.get_test_mode()
        return {"test_mode": test_mode}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
