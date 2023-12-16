""" general utilities for DB and logic functions """
from typing import List, Tuple, Dict, Union

from api.models.models import AddTransaction, Payment


def api_address_to_db_table(address_account: str) -> str:
    """api_address_to_db_table

    Api routes do not match the table names exactly (for human-readability vs. machine), so this
    converts those values across the table.

    Args:
        address_account (str): name of the account or table from the API

    Returns:
        str: name of the account or table for the DB table
    """
    account_list = address_account.split('_')
    account_list = [word.capitalize() for word in account_list]
    try:
        index = account_list.index('And')
        account_list[index] = 'and'
    except: # pylint: disable=bare-except
        pass
    account = " ".join(account_list)
    return account


def transaction_payers_and_debtors(
        add_transaction: Union[AddTransaction, Payment],
        people: List[str],
        is_settle_up: bool = False
    ) -> Tuple[Dict[str, float], Dict[str, float]]:
    """transaction_payers_and_debtors

    Formats and sets up who owes what for payments off a transaction (including a settle up
    transaction).

    Format:
    paid, owes
    {personA: $xx.xx, personB: $yy.yy}, {personA: $xx.xx, personB: $yy.yy}

    Args:
        add_transaction (Union[AddTransaction, Payment]): A payment or transaction API object
        people (List[str]): list of people involved
        is_settle_up (bool, optional): special case for settling up. Defaults to False.

    Returns:
        Tuple[Dict[str, float], Dict[str, float]]: paid object, owes object
    """
    if is_settle_up:
        paid = {add_transaction.payer: add_transaction.amount}
        owes = {add_transaction.payer: 0.0}
    else:
        paid = {add_transaction.paid_by_name: round(add_transaction.paid_amount, 2)}
        owes = {add_transaction.paid_by_name: 0.0}
    for person in people:
        if person not in paid:
            paid[person] = 0.0
        if person not in owes:
            if is_settle_up:
                owes[person] = round(add_transaction.amount, 2)
            else:
                owes[person] = round(add_transaction.other_person_owes, 2)
    return paid, owes
        