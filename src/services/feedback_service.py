from pydantic import ValidationError

from src.data_models.feedback_data_models import FeedbackRatings, FeedbackSubmission
from datetime import datetime, timezone
from src.utils.record_id import generate_id
from src.repositories.feedback_repository import FeedbackRepository


class FeedbackService:
    """
    Manage feedback
    """

    feedback_repository = FeedbackRepository()

    def get_feedback_submissions(self) -> list[FeedbackSubmission]:
        try:
            results = self.feedback_repository.get_all_feedback()
            submissions = [FeedbackSubmission(**result) for result in results]
        except ValidationError as ve:
            raise Exception(f"Validation error while processing feedback submissions: {str(repr(ve.errors()))}")
        except Exception as ex:
            raise Exception(f"Failed to fetch feedback submissions: {str(ex)}")
        return submissions

    def submit_feedback(self, message: str, ratings: FeedbackRatings, email_address: str = ""):
        """
        Submit feedback to the database.
        :param message:
        :param ratings:
        :param email_address:
        :return:
        """
        feedback_id = generate_id()
        feedback = FeedbackSubmission(
            feedback_id=feedback_id,
            message=message,
            ratings=ratings,
            email_address=email_address,
            timestamp=datetime.now(tz=timezone.utc),
        )
        result = self.feedback_repository.create_feedback(feedback=feedback)
        if not result:
            raise Exception("Failed to submit feedback")
        return result

    def delete_feedback(self, feedback_id: str) -> bool:
        """
        Delete feedback by ID.
        :param feedback_id: The ID of the feedback to delete.
        :return: True if deletion was successful, False otherwise.
        """
        try:
            result = self.feedback_repository.delete_feedback(feedback_id=feedback_id)
            if result.deleted_count == 0:
                raise Exception(f"Feedback with ID {feedback_id} not found or already deleted")
            return True
        except Exception as ex:
            print(ex)
            raise Exception(f"Failed to delete feedback: {str(ex)}")
