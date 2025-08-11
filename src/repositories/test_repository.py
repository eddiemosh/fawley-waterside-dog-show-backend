from src.utils.database import Database


class TestRepository:
    def __init__(self):
        self.collection = Database().get_collection("test")

    def get_test_mode(self):
        result = self.collection.find_one()
        if not result:
            self.create_test_mode()
            self.get_test_mode()
        return result.get("test_mode")

    def create_test_mode(self):
        if len(self.collection.find_one()) > 0:
            raise Exception("Test mode already exists")
        result = self.collection.insert_one({"test_mode": False})
        if not result.acknowledged:
            raise Exception("Failed to create test mode")
        return result

    def toggle_test_mode(self):
        current_mode = self.get_test_mode()
        new_mode = not current_mode
        result = self.collection.update_one({}, {"$set": {"test_mode": new_mode}})
        if result.modified_count == 0:
            raise Exception("Failed to toggle test mode")
        return new_mode
