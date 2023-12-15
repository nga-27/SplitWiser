""" Models for FastAPI and DB strucutures """
from typing import Optional

from pydantic import BaseModel


class AddTransaction(BaseModel):
    """ Object to add a transaction (different than transaction as the fields are easier to use for
    an API input)"""
    item: str
    paid_by_name: str
    paid_amount: float
    other_person_owes: float

class Transaction(BaseModel):
    """ Transaction record object """
    id: Optional[str] = "0"
    date: Optional[str] = ""
    item: str
    paid_by_id: dict # {person_name: amount, person_name...}
    owed_by_id: dict # {person_name: amount, person_name...}

class Payment(BaseModel):
    """ Payment record object """
    id: Optional[str] = "0"
    date: Optional[str] = ""
    account: str
    payer: str
    amount: float
