import datetime

from api.libs.db import get_db, post_to_db
from api.models.models import AddTransaction, Transaction

def get_all_transactions(ledger_sheet: str) -> dict:
    return get_db()[ledger_sheet]


def add_transaction(add_transaction: AddTransaction, ledger_sheet: str):
    DB = get_db()
    num_records = len(DB[ledger_sheet])
    people = DB['People']['__list__']

    paid = {add_transaction.paid_by_name: round(add_transaction.paid_amount, 2)}
    owes = {add_transaction.paid_by_name: 0}
    for person in people:
        if person not in paid:
            paid[person] = 0
        if person not in owes:
            owes[person] = round(add_transaction.other_person_owes, 2)

    record = Transaction(
        date=datetime.datetime.now().strftime("%m/%d/%Y"),
        id=str(num_records),
        item=add_transaction.item,
        paid_by_id=paid,
        owed_by_id=owes
    ).dict()
    post_to_db(record, record["id"], ledger_sheet)
    return