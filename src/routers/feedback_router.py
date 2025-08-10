from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, HTTPException
from starlette.requests import Request

from src.services.email import EmailService
from src.services.feedback import FeedbackService
from src.services.orders import OrderService

router = APIRouter(prefix="/feedback", tags=["Feedback"])


feedback_service = FeedbackService()


@router.get("", status_code=HTTPStatus.OK)
def get_feedback_submissions():
    """
    Get all feedback submissions.
    :return:
    """
    try:
        feedback_data = feedback_service.get_feedback_submissions()
        if not feedback_data:
            raise HTTPException(status_code=404, detail="No feedback data found.")
        return feedback_data
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@router.post("/submit", status_code=HTTPStatus.OK)
def submit_feedback(
        request: Request
):
    """
    Create feedback submission.
    :return:
    """
    try:
        feedback_service.submit_feedback(text=request.get("feedback"), email_address=request.get("email_address"), ratings=request.get("ratings"))
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
