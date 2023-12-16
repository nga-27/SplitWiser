""" transaction logic handlers """
import datetime
from typing import Union, Dict

from api.libs.db import get_db, post_to_db, patch_entire_table, reorder_table
from api.libs.summary import update_summary
from api.libs.utils import transaction_payers_and_debtors
from api.models.models import AddTransaction, Transaction


def get_transactions(table_name: str, _id: Union[str, None] = None) -> dict:
    """get_transactions

    Returns all transactions of a particular account / table name or an individual transaction (when
    _id is not None)

    Args:
        table_name (str): table name (account name)
        _id (Union[str, None], optional): ID of a particular object, else all transactions of a
                                        particular account. Defaults to None.

    Returns:
        dict: all transactions of a particular account or a particular transaction (id not None)
    """
    ledger = get_db()[table_name]
    if _id is None:
        return ledger
    return ledger.get(str(_id))


def delete_transaction(_id: str, table_name: str) -> Union[Dict[str, dict], None]:
    """delete_transaction

    Deletes a transaction from the DB

    Args:
        _id (str): id of the transaction to remove
        table_name (str): table name

    Returns:
        Union[Dict[str, dict], None]: returns the deleted object if it exists
    """
    ledger = get_db()[table_name]
    if _id not in ledger:
        return None
    transaction = ledger.pop(_id)
    patch_entire_table(ledger, table_name)
    reorder_table(table_name)
    update_summary()
    return transaction


def add_transaction(transaction_to_add: AddTransaction, table_name: str) -> None:
    """add_transaction

    Logic of adding transaction from the api to the DB

    Args:
        transaction_to_add (AddTransaction): AddTransaction object from the API
        table_name (str): table name
    """
    _db = get_db()
    people = _db['People']['__list__']
    paid, owes = transaction_payers_and_debtors(transaction_to_add, people)

    record = Transaction(
        date=datetime.datetime.now().strftime("%m/%d/%Y"),
        item=transaction_to_add.item,
        paid_by_id=paid,
        owed_by_id=owes,
        id='0'
    ).dict()
    post_to_db(record, table_name)
    update_summary()
