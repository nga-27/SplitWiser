""" delete transaction handler for cmd_app """
import time

from cmd_app.utils.prompts import intro_and_choose_account, input_id_handler
from cmd_app.utils.ui import format_transactions
from cmd_app.utils.api import handle_delete_id, handle_get_payload
from cmd_app.utils.constants import PrintColor


def pick_transaction_to_delete(num_transactions: int) -> str:
    """pick_transaction_to_delete

    Walks user through prompts to find ID of transaction to delete

    Args:
        num_transactions (int): total number of transactions in the account

    Returns:
        str: _id of the transaction to delete
    """
    time.sleep(1)
    id_ = ""
    while id_ == "":
        input_str = "\r\nSeeing the transaction IDs above, which one to delete? ('menu' to return "
        input_str += "to main menu) "
        id_str = input(input_str)
        id_ = input_id_handler(id_str, num_transactions)
        if id_ == "menu":
            break
        if id_ == "":
            continue

        msg = "To clarify, you wish to delete transaction "
        msg += f"{PrintColor.RED}#{id_}{PrintColor.NORMAL}, "
        msg += "correct? (enter is yes, 'N' to redo) "
        validate = input(msg)
        validate = validate.strip()
        if 'N' in validate.upper():
            id_ = ""
    return id_


def is_account_empty(num_transactions: int) -> bool:
    """is_account_empty

    Not only a check but with prompts and prints

    Args:
        num_transactions (int): number of transactions

    Returns:
        bool: if the account is empty or has transactions in it
    """
    if num_transactions == 0:
        print("\r\nSorry, there are no transactions to delete here!")
        time.sleep(2)
        print("\r\n")
        return True
    return False

##########################################

def delete_handler(base_url: str) -> bool:
    """delete_handler

    Top-level transaction deletion handler

    Args:
        base_url (str): base url of API

    Returns:
        bool: True to continue the prompts
    """
    account, color = intro_and_choose_account(
        "Deleting requires the 'id' of the transaction.", is_for_payment=True)
    transactions = handle_get_payload(f"{base_url}/transactions/{account}")
    if is_account_empty(len(transactions)):
        return True

    format_transactions(transactions, account, color=color)
    id_to_delete = pick_transaction_to_delete(len(transactions))
    if id_to_delete == "menu":
        return True

    deleted_item = handle_delete_id(f"{base_url}/transactions/{account}/{id_to_delete}")
    if deleted_item is not None:
        msg = f"\r\n\r\n'{PrintColor.RED}{deleted_item['item']}{PrintColor.NORMAL}' "
        msg += "successfully deleted!"
        print(msg)
    else:
        print(f"\r\n\r\nSomething went wrong, as transaction #{id_to_delete} failed to delete.")
    time.sleep(3)
    print("\r\n")
    return True
