import datetime

from api.libs.db import get_db, post_to_db
from api.models.models import AddTransaction, Transaction

def get_all_transactions(ledger_sheet: str) -> dict:
    return get_db()[ledger_sheet]


def add_transaction(add_transaction: AddTransaction, ledger_sheet: str):
    DB = get_db()
    num_records = len(DB[ledger_sheet])
    people = DB['People']['__list__']

    paid = [{add_transaction.paid_by_name: add_transaction.paid_amount}]
    owes = [{add_transaction.paid_by_name: 0}]
    owe_names = []
    for item in owes:
        for val in item.keys():
            owe_names.append(val)
    paid_names = []
    for item in paid:
        for val in item.keys():
            paid_names.append(val)
    for person in people:
        if person not in paid_names:
            paid.append({person: 0})
        if person not in owe_names:
            owes.append({person: add_transaction.other_person_owes})

    record = Transaction(
        date=datetime.datetime.now().strftime("%m/%d/%Y"),
        id=str(num_records),
        item=add_transaction.item,
        paid_by_id=paid,
        owed_by_id=owes
    ).dict()
    post_to_db(record, record["id"], ledger_sheet)
    return