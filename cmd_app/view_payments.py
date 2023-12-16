""" view payments / settle ups made for main cmd_app """
import time

from cmd_app.utils.api import handle_get_payload
from cmd_app.utils.ui import format_payments
from cmd_app.utils.constants import PrintColor


def view_payments_handler(base_url: str) -> bool:
    """view_payments_handler

    Top-level handler for viewing payments made (settle ups)

    Args:
        base_url (str): api base url

    Returns:
        bool: True to keep the prompts looping
    """
    msg = "\r\nCool. Let's get right to the "
    msg += f"{PrintColor.HIGHLIGHT}payment history{PrintColor.NORMAL}..."
    print(msg)
    time.sleep(1)
    payments = handle_get_payload(f"{base_url}/payments/")
    format_payments(payments)
    time.sleep(4)
    return True
