import time

from cmd_app.utils.prompts import intro_and_choose_account
from cmd_app.utils.api import handle_get_payload
from cmd_app.utils.ui import format_balances


def view_balances_handler(base_url: str) -> bool:
    print("\r\nCool. Let's get right to the balances...")
    time.sleep(1)
    balances = handle_get_payload(f"{base_url}/summary/")
    format_balances(balances)
    return True