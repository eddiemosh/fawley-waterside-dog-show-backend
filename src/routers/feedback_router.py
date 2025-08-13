from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from src.data_models.feedback_data_models import FeedbackRatings
from src.services.feedback_service import FeedbackService

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
        ratings = FeedbackRatings(**payload.get("ratings"))
    except Exception as ex:
        raise HTTPException(status_code=400, detail=f"Invalid ratings format: {str(ex)}")
    try:
        feedback_service.submit_feedback(
            message=payload.get("feedback"), email_address=payload.get("email_address"), ratings=ratings
        )
        return {"status": "success"}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@router.delete("/delete", status_code=HTTPStatus.OK)
def delete_feedback(feedback_id: str):
    """
    Delete feedback submission by ID.
    :param feedback_id: The ID of the feedback submission to delete.
    :return: A message indicating the deletion status.
    """
    try:
        if not feedback_id:
            raise HTTPException(status_code=400, detail="Feedback ID is required.")
        feedback_service.delete_feedback(feedback_id=feedback_id)
        return {"message": "Feedback deleted successfully."}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
