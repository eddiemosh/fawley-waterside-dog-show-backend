from src.data_models.feedback_data_models import FeedbackRatings
from src.data_models.order_data_models import Order
from src.services.database import Database


class FeedbackService:
    """
    Manage feedback
    """

    database_service = Database()

    def submit_feedback(
        self,
        text: str,
        ratings: FeedbackRatings,
        email_address: str = "",
    ):
        """
        Submit feedback to the database.
        :param text: the feedback text
        :param ratings: the ratings given by the user
        :param email_address: the email address of the user submitting feedback
        :return:
        """

    def get_feedback_submission(self, order_id: str):
        result = self.database_service.sumbit_feedback(order_id=order_id)
        return Order(**result)

    def get_feedback_submissions(self):
        results = self.database_service.get_orders()
        orders = [Order(**result) for result in results]
        return orders

    def delete_order(self, order_id: str):
        result = self.database_service.delete_order(order_id=order_id)
        return result
