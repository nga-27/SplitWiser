import time

from cmd_app.utils.prompts import intro_and_choose_account
from cmd_app.utils.api import handle_get_payload
from cmd_app.utils.ui import format_transactions
from cmd_app.utils.constants import PrintColor


def view_handler(base_url: str) -> bool:
    color = PrintColor()
    msg = f"Sweet, let's check out the {color.CYAN}TRANSACTIONS{color.NORMAL} that exist."
    account, color = intro_and_choose_account(msg)
    transactions = handle_get_payload(f"{base_url}/transactions/{account}")
    format_transactions(transactions, account, color=color)
    time.sleep(4)
    return True
