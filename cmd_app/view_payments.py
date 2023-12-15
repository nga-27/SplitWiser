import time

from cmd_app.utils.api import handle_get_payload
from cmd_app.utils.ui import format_payments
from cmd_app.utils.constants import PrintColor


def view_payments_handler(base_url: str) -> bool:
    print(f"\r\nCool. Let's get right to the {PrintColor.HIGHLIGHT}payment history{PrintColor.NORMAL}...")
    time.sleep(1)
    payments = handle_get_payload(f"{base_url}/payments/")
    format_payments(payments)
    time.sleep(4)
    return True