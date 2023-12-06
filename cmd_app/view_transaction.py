import time

from .utils import which_account, handle_get_payload, format_transactions


def intro_and_choose_account() -> str:
    print("\r\nSweet, let's check out the transactions that exist.\r\n")
    time.sleep(1)
    account = which_account()
    account_list = account.lower().split(' ')
    account_url = '_'.join(account_list)
    return account_url

##########################################

def view_handler(base_url: str) -> bool:
    account = intro_and_choose_account()
    transactions = handle_get_payload(f"{base_url}/transactions/{account}")
    str_transactions = format_transactions(transactions)
    print(str_transactions)
    return True