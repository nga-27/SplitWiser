from typing import Optional, List
import uuid
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
    id: Optional[str] = uuid.uuid4()
    date: Optional[str] = datetime.datetime.now().strftime("%m/%d/%Y")
    item: str
    paid_by: Person
    amount: float
    owed_by_involved: List[TransactionalDebt]
