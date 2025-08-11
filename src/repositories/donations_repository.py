from src.data_models.donation_data_models import Donation
from src.utils.database import Database


class DonationsRepository:
    def __init__(self):
        self.collection = Database().get_collection("donations")
        try:
            self.collection.create_index("donation_id", unique=True)
        except Exception as ex:
            print(f"Error creating index on 'donation_id': {ex}")

    def create_donation(self, donation: Donation):
        return self.collection.insert_one(donation.model_dump())

    def get_all_donations(self) -> list[dict]:
        return list(self.collection.find())

    def get_donation(self, donation_id: str) -> dict:
        result = self.collection.find_one({"donation_id": donation_id})
        if not result:
            raise Exception(f"Donation with ID {donation_id} not found")
        return result
