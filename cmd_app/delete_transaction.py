import time

from cmd_app.utils.prompts import intro_and_choose_account
from cmd_app.utils.ui import format_transactions
from cmd_app.utils.api import handle_delete_id, handle_get_payload

def pick_transaction_to_delete(num_transactions: int) -> int:
    time.sleep(1)
    id_ = -1
    while id_ == -1:
        id_str = input("\r\n\r\nSeeing the transaction IDs above, which one to delete? ('menu' to return to main menu) ")
        id_str = id_str.strip()
        if 'menu' in id_str.lower():
            return -1
        try:
            id_ = int(id_str)
            if id_ > num_transactions - 1 or id_ < 0:
                print(f"'{id_}' is not in range of 0 - {num_transactions - 1}. Please try again.\r\n")
                time.sleep(1)
                id_ = -1
                continue
        except:
            print(f"'{id_}' is not a valid number in range of 0 - {num_transactions - 1}. Please try again.\r\n")
            time.sleep(1)
            id_ = -1

        validate = input(f"To clarify, you wish to delete transaction #{id_}, correct? (enter is yes, 'N' to redo) ")
        validate = validate.strip()
        if 'N' in validate.upper():
            id_ = -1
    return id_

##########################################

def delete_handler(base_url: str) -> bool:
    account = intro_and_choose_account("Deleting requires the 'id' of the transaction.")
    transactions = handle_get_payload(f"{base_url}/transactions/{account}")
    str_transactions = format_transactions(transactions)
    print(str_transactions)
    id_to_delete = pick_transaction_to_delete(len(transactions))
    if id_to_delete == -1:
        return True
    
    if handle_delete_id(f"{base_url}/transactions/{account}/{id_to_delete}"):
        print(f"\r\n\r\n#{id_to_delete} successfully deleted!")
    else:
        print(f"\r\n\r\nSomething went wrong, as transaction #{id_to_delete} failed to delete.")
    return True