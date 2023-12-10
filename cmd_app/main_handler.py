import time

from cmd_app.add_transaction import add_handler
from cmd_app.view_transaction import view_handler
from cmd_app.delete_transaction import delete_handler
from cmd_app.record_payment import record_handler
from cmd_app.view_balances import view_balances_handler

from cmd_app.utils.api import handle_get_payload
from cmd_app.utils.constants import PrintColor
from cmd_app.utils.title_page import show_title

OPTION_STATES = {
    "v": "view",
    "view": "view",
    "a": "add",
    "add": "add",
    "d": "delete",
    "delete": "delete",
    "s": "record",
    "settle": "record",
    "b": "balance",
    "balance": "balance",
    "e": "exit",
    "exit": "exit"
}

def exit_handler(_: str) -> bool:
    print("\r\nWe'll start to exit...\r\n")
    time.sleep(1)
    return False


ACTION_FUNCTIONS = {
    "balance": view_balances_handler,
    "view": view_handler,
    "add": add_handler,
    "delete": delete_handler,
    "record": record_handler,
    "exit": exit_handler
}


def what_to_do_options():
    matched = None
    color = PrintColor()
    while matched is None:
        options = "What would you like to do? Options include:\r\n\r\n"
        options += f"\t- View {color.MAGENTA}BALANCES{color.NORMAL} between "
        options += "accounts (b or balance)\r\n"
        options += f"\t- View {color.CYAN}TRANSACTIONS{color.NORMAL} (v or view)\r\n"
        options += f"\t- {color.GREEN}ADD{color.NORMAL} transactions (a or add)\r\n"
        options += f"\t- {color.RED}DELETE{color.NORMAL} Transaction (d or delete)\r\n"
        options += f"\t- {color.BLUE}SETTLE UP{color.NORMAL} / make a payment (s or settle)\r\n"
        options += f"\t- {color.YELLOW}EXIT{color.NORMAL} (e or exit)"
        print(options)
        passed = input("\r\nSo... what would you like to do? ")
        passed = passed.lower().strip()
        matched = OPTION_STATES.get(passed)
        if not matched:
            print(f"\r\nI'm sorry, but '{passed}' is not a valid input. Please try again...\r\n")
            time.sleep(2)
    return matched

###################################################

def run(base_url: str):
    is_running = True
    while is_running:
        action = what_to_do_options()
        is_running = ACTION_FUNCTIONS[action](base_url)


def startup(base_url: str) -> None:
    show_title()
    has_succeeded = False
    while not has_succeeded:
        try:
            handle_get_payload(f"{base_url}/start", skip_response=True)
            has_succeeded = True
        except:
            pass
        time.sleep(2)


def shutdown(base_url: str) -> None:
    print("\r\nShutting down...")
    handle_get_payload(f"{base_url}/shutdown", skip_response=True)
