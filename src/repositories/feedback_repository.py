from src.data_models.feedback_data_models import FeedbackSubmission
from src.utils.database import Database


class FeedbackRepository:
    def __init__(self):
        self.collection = Database().get_collection("feedback")
        try:
            self.collection.create_index("feedback_id", unique=True)
        except Exception as ex:
            print(f"Error creating index on 'feedback_id': {ex}")

    def create_feedback(self, feedback: FeedbackSubmission):
        return self.collection.insert_one(feedback.model_dump())

    def get_all_feedback(self):
        return list(self.collection.find())

    def delete_feedback(self, feedback_id: str):
        return self.collection.delete_one({"feedback_id": feedback_id})
