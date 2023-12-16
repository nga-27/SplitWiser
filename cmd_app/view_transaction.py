""" view transactions for main cmd_app """
import time

from cmd_app.utils.prompts import intro_and_choose_account
from cmd_app.utils.api import handle_get_payload
from cmd_app.utils.ui import format_transactions
from cmd_app.utils.constants import PrintColor


def view_handler(base_url: str) -> bool:
    """view_handler

    View transactions for a particular account

    Args:
        base_url (str): api base url

    Returns:
        bool: True to keep the prompt looping
    """
    msg = f"Sweet, let's check out the {PrintColor.CYAN}TRANSACTIONS{PrintColor.NORMAL} that exist."
    account, color = intro_and_choose_account(msg)
    transactions = handle_get_payload(f"{base_url}/transactions/{account}")
    format_transactions(transactions, account, color=color)
    time.sleep(4)
    return True
