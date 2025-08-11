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
