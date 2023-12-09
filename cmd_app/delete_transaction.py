import time

from cmd_app.utils.prompts import intro_and_choose_account, input_id_handler
from cmd_app.utils.ui import format_transactions
from cmd_app.utils.api import handle_delete_id, handle_get_payload

def pick_transaction_to_delete(num_transactions: int) -> str:
    time.sleep(1)
    id_ = ""
    while id_ == "":
        id_str = input("\r\n\r\nSeeing the transaction IDs above, which one to delete? ('menu' to return to main menu) ")
        id_ = input_id_handler(id_str, num_transactions)
        if id_ == "menu":
            break
        if id_ == "":
            continue

        validate = input(f"To clarify, you wish to delete transaction #{id_}, correct? (enter is yes, 'N' to redo) ")
        validate = validate.strip()
        if 'N' in validate.upper():
            id_ = ""
    return id_

def is_account_empty(num_transactions: int) -> bool:
    if num_transactions == 0:
        print("\r\nSorry, there are no transactions to delete here!")
        time.sleep(2)
        print("\r\n")
        return True
    return False

##########################################

def delete_handler(base_url: str) -> bool:
    account = intro_and_choose_account("Deleting requires the 'id' of the transaction.")
    transactions = handle_get_payload(f"{base_url}/transactions/{account}")
    if is_account_empty(len(transactions)):
        return True

    format_transactions(transactions, account)
    id_to_delete = pick_transaction_to_delete(len(transactions))
    if id_to_delete == "menu":
        return True
    
    if handle_delete_id(f"{base_url}/transactions/{account}/{id_to_delete}"):
        print(f"\r\n\r\n#{id_to_delete} successfully deleted!")
    else:
        print(f"\r\n\r\nSomething went wrong, as transaction #{id_to_delete} failed to delete.")
    return True