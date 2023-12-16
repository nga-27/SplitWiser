""" view balances (summary) for main cmd_app """
import time

from cmd_app.utils.api import handle_get_payload
from cmd_app.utils.ui import format_balances
from cmd_app.utils.constants import PrintColor


def view_balances_handler(base_url: str) -> bool:
    """view_balances_handler

    Top-level viewing of balances / summary

    Args:
        base_url (str): api base url

    Returns:
        bool: True to keep the main looping going for prompts
    """
    print(f"\r\nCool. Let's get right to the {PrintColor.MAGENTA}balances{PrintColor.NORMAL}...")
    time.sleep(1)
    balances = handle_get_payload(f"{base_url}/summary/")
    format_balances(balances)
    time.sleep(4)
    return True
