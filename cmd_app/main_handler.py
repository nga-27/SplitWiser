import time

from cmd_app.add_transaction import add_handler
from cmd_app.view_transaction import view_handler
from cmd_app.delete_transaction import delete_handler
from cmd_app.record_payment import record_handler

OPTION_STATES = {
    "--v": "view",
    "--a": "add",
    "--d": "delete",
    "--r": "record",
    "--e": "exit",
    "exit": "exit"
}

def exit_handler() -> bool:
    print("\r\nWe'll start to exit...\r\n")
    time.sleep(1)
    return False


ACTION_FUNCTIONS = {
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
        options += "\t- View Transactions (--v)\r\n"
        options += "\t- Add Transaction (--a)\r\n"
        options += "\t- Delete Transaction (--d)\r\n"
        options += "\t- Record Payment / Settle Up (--r)\r\n"
        options += "\t- Exit (--e or exit)"
        print(options)
        passed = input("\r\nSo... what would you like to do? ")
        passed = passed.lower().strip()
        matched = OPTION_STATES.get(passed)
        if not matched:
            print(f"\r\nI'm sorry, but '{passed}' is not a valid input. Please try again...\r\n")
            time.sleep(2)
    return matched

###################################################

def run():
    is_running = True
    while is_running:
        action = what_to_do_options()
        is_running = ACTION_FUNCTIONS[action]()
