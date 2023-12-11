import datetime
from typing import Union

from api.libs.db import get_db, post_to_db, patch_entire_table, reorder_table
from api.libs.summary import update_summary
from api.libs.utils import transaction_payers_and_debtors
from api.models.models import AddTransaction, Transaction


def get_transactions(ledger_sheet: str, id: Union[str, None] = None) -> dict:
    ledger = get_db()[ledger_sheet]
    if id is None:
        return ledger
    return ledger.get(str(id))

def delete_transaction(id: str, ledger_sheet: str) -> Union[dict, None]:
    ledger = get_db()[ledger_sheet]
    if id not in ledger:
        return None
    transaction = ledger.pop(id)
    patch_entire_table(ledger, ledger_sheet)
    reorder_table(ledger_sheet)
    update_summary()
    return transaction


def add_transaction(add_transaction: AddTransaction, ledger_sheet: str):
    DB = get_db()
    people = DB['People']['__list__']
    paid, owes = transaction_payers_and_debtors(add_transaction, people)

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

