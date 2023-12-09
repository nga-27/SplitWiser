import time

from cmd_app.add_transaction import add_handler
from cmd_app.view_transaction import view_handler
from cmd_app.delete_transaction import delete_handler
from cmd_app.record_payment import record_handler
from cmd_app.view_balances import view_balances_handler

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
    while matched is None:
        options = "What would you like to do? Options include:\r\n\r\n"
        options += "\t- View BALANCES between accounts (b or balance)\r\n"
        options += "\t- View TRANSACTIONS (v or view)\r\n"
        options += "\t- ADD transactions (a or add)\r\n"
        options += "\t- DELETE Transaction (d or delete)\r\n"
        options += "\t- SETTLE UP / make a payment (s or settle)\r\n"
        options += "\t- EXIT (e or exit)"
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
