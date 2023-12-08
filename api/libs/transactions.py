import datetime
from typing import Union

from api.libs.db import get_db, post_to_db, patch_entire_table
from api.libs.summary import update_summary
from api.models.models import AddTransaction, Transaction


def get_transactions(ledger_sheet: str, id: Union[str, None] = None) -> dict:
    ledger = get_db()[ledger_sheet]
    if id is None:
        return ledger
    return ledger.get(str(id))

def delete_transaction(id: str, ledger_sheet: str) -> Union[None, str]:
    ledger = get_db()[ledger_sheet]
    if id not in ledger:
        return f"Transaction id '{id}' not found."
    ledger.pop(id)
    patch_entire_table(ledger, ledger_sheet)
    update_summary()
    return None


def add_transaction(add_transaction: AddTransaction, ledger_sheet: str):
    DB = get_db()
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
        item=add_transaction.item,
        paid_by_id=paid,
        owed_by_id=owes,
        id='0'
    ).dict()
    post_to_db(record, ledger_sheet)
    update_summary()
    return

