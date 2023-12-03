from typing import Optional, List
import datetime

from pydantic import BaseModel


class Person(BaseModel):
    id: str # "0"
    name: str

class TransactionalDebt(BaseModel):
    id: str
    person: Person
    amount: float

class Transaction(BaseModel):
    id: str
    date: Optional[str] = datetime.datetime.now().strftime("%m/%d/%Y")
    item: str
    paid_by_id: list # List[TransactionalDebt] as {person_id: amount}
    owed_by_id: list # List[TransactionalDebt] as {person_id: amount}
