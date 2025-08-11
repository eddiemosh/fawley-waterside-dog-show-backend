from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, HTTPException, Request
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
def submit_feedback(payload: dict):
    """
    Create feedback submission.
    Expects payload: {"feedback": str, "email_address": str, "ratings": {...}}
    """
    try:
        feedback_service.submit_feedback(
            text=payload.get("feedback"),
            email_address=payload.get("email_address"),
            ratings=payload.get("ratings")
        )
        return {"status": "success"}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
