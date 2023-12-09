import time

from cmd_app.utils.prompts import intro_and_choose_account
from cmd_app.utils.api import handle_get_payload
from cmd_app.utils.ui import format_transactions


def view_handler(base_url: str) -> bool:
    account = intro_and_choose_account("Sweet, let's check out the transactions that exist.")
    transactions = handle_get_payload(f"{base_url}/transactions/{account}")
    format_transactions(transactions, account)
    time.sleep(5)
    return True
