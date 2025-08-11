from src.data_models.feedback_data_models import FeedbackRatings, FeedbackSubmission
from src.services.database import Database


class FeedbackService:
    """
    Manage feedback
    """

    database_service = Database()

    def get_feedback_submissions(self):
        results = self.database_service.get_feedback_submissions()
        submissions = [FeedbackSubmission(**result) for result in results]
        return submissions

    def submit_feedback(self, text: str, ratings: FeedbackRatings, email_address: str = ""):
        """
        Submit feedback to the database.
        :param text:
        :param ratings:
        :param email_address:
        :return:
        """

        result = self.database_service.create_feedback_submission(
            text=text, ratings=ratings, email_address=email_address
        )
        if not result:
            raise Exception("Failed to submit feedback")
        return result
