from typing import Optional

from pydantic import BaseModel


class Person(BaseModel):
    id: str # "0"
    name: str

class TransactionalDebt(BaseModel):
    id: str
    person: Person
    amount: float

class AddTransaction(BaseModel):
    item: str
    paid_by_name: str
    paid_amount: float
    other_person_owes: float

class Transaction(BaseModel):
    id: Optional[str] = "0"
    date: Optional[str] = ""
    item: str
    paid_by_id: dict # Dict[TransactionalDebt] as {person_name: amount, person_name...}
    owed_by_id: dict # List[TransactionalDebt] as {person_name: amount, person_name...}
