from pydantic import ValidationError

from src.data_models.feedback_data_models import FeedbackRatings, FeedbackSubmission
from src.services.database import Database
from src.utils.record_id import generate_id


class FeedbackService:
    """
    Manage feedback
    """

    database_service = Database()

    def get_feedback_submissions(self) -> list[FeedbackSubmission]:
        try:
            results = self.database_service.get_feedback_submissions()
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
        result = self.database_service.create_feedback_submission(
            feedback_id=feedback_id,
            message=message, ratings=ratings, email_address=email_address
        )
        if not result:
            raise Exception("Failed to submit feedback")
        return result
