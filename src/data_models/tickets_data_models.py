from pydantic import BaseModel


class PedigreeTickets(BaseModel):
    any_puppy: int = 0
    any_junior: int = 0
    any_gundog: int = 0
    any_utility: int = 0
    any_hound: int = 0
    any_toy: int = 0
    any_working: int = 0
    any_pastoral: int = 0
    any_terrier: int = 0
    any_open: int = 0
    any_veteran: int = 0
    junior_handler: int = 0


class AllDogTickets(BaseModel):
    puppy: int = 0
    prettiest: int = 0
    best_condition: int = 0
    best_rescue: int = 0
    waggiest_tale: int = 0
    childs_best_friend: int = 0
    fancy_dress: int = 0
    handsome: int = 0
    fluffiest: int = 0
    scruffiest: int = 0
    smooth: int = 0
    looks_like_owner: int = 0
    obedience: int = 0
    golden_oldie: int = 0
