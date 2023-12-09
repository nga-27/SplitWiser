from typing import List, Tuple, Dict, Union

from api.models.models import AddTransaction, Payment


def api_address_to_db_table(address_account: str) -> str:
    account_list = address_account.split('_')
    account_list = [word.capitalize() for word in account_list]
    try:
        index = account_list.index('And')
        account_list[index] = 'and'
    except:
        pass
    account = " ".join(account_list)
    return account


def transaction_payers_and_debtors(
        add_transaction: Union[AddTransaction, Payment],
        people: List[str],
        is_settle_up: bool = False
    ) -> Tuple[Dict[str, float], Dict[str, float]]:
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
        