from typing import Optional

from pydantic import BaseModel


class PedigreeTickets(BaseModel):
    any_puppy: Optional[int] = None
    any_junior: Optional[int] = None
    any_gundog: Optional[int] = None
    any_utility: Optional[int] = None
    any_hound: Optional[int] = None
    any_toy: Optional[int] = None
    any_working: Optional[int] = None
    any_pastoral: Optional[int] = None
    any_terrier: Optional[int] = None
    any_open: Optional[int] = None
    any_veteran: Optional[int] = None
    junior_handler: Optional[int] = None


class AllDogTickets(BaseModel):
    puppy: Optional[int] = None
    prettiest: Optional[int] = None
    best_condition: Optional[int] = None
    best_rescue: Optional[int] = None
    waggiest_tale: Optional[int] = None
    childs_best_friend: Optional[int] = None
    fancy_dress: Optional[int] = None
    handsome: Optional[int] = None
    fluffiest: Optional[int] = None
    scruffiest: Optional[int] = None
    smooth: Optional[int] = None
    looks_like_owner: Optional[int] = None
    obedience: Optional[int] = None
    golden_oldie: Optional[int] = None
