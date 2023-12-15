import time

from cmd_app.utils.api import handle_get_payload
from cmd_app.utils.ui import format_balances
from cmd_app.utils.constants import PrintColor


def view_balances_handler(base_url: str) -> bool:
    print(f"\r\nCool. Let's get right to the {PrintColor.MAGENTA}balances{PrintColor.NORMAL}...")
    time.sleep(1)
    balances = handle_get_payload(f"{base_url}/summary/")
    format_balances(balances)
    time.sleep(4)
    return True