import time

from cmd_app.utils.prompts import which_account, who_paid
from cmd_app.utils.api import handle_post
from cmd_app.utils.constants import OTHER_PERSON


def get_valid_name(message: str) -> str:
    print("")
    name2 = "N"
    while 'N' in name2:
        name = input(f"{message} ")
        name2 = input(f"Nice. Cool with '{name}'? (just hit enter if yes, or 'N' if to redo it.)").upper()
    return name

def get_valid_amount(message: str) -> float:
    amt = -1.0
    while amt < 0.0:
        print("")
        ew_input = input(f"{message} ")
        if '$' in ew_input:
            ew_input = ew_input.split('$')[-1]
            ew_input = ew_input.strip()
        try:
            amt = float(ew_input)
            if amt < 0.0:
                print("I'm sorry, but a payment must be $0 or more.")
                time.sleep(2)
                continue
        except ValueError:
            amt = -1.0
            print("I'm sorry, that didn't seem to be a valid amount. Try in the form of XXX.YY or XXX.")
            time.sleep(2)
            continue

        verify = input(f"Are you happy with the amount of ${amt}? (enter or yes) ")
        if verify != '' and verify.lower() != 'yes':
            amt = -1.0
    return amt

def how_to_split_transaction(amt: float, who_paid: str) -> float:
    """ returns what the other person pays """
    OPTION_SPLITS = ["50% / 50%", "100% the other person", f"100% {who_paid}, so no one owes",
                     "60% Nick, 40% Jill", "Custom"]
    OPTION_MATH = [0.5, 1.0, 0.0, 0.4, 1.0]
    if who_paid == 'Jill':
        OPTION_MATH[3] = 0.6

    valid_split = False
    while not valid_split:
        print("\r\nHow would you like to split the transaction? ")
        options = "Options include:\r\n\r\n"
        for i in range(1, len(OPTION_SPLITS) + 1):
            options += f"\t{i}. {OPTION_SPLITS[i-1]}\r\n"
        print(options)
        split_option = input("\r\nEnter the number (1-5) for the option you want: ")
        try:
            split_option = int(split_option.strip())
            valid_split = True
        except:
            print(f"\r\nSorry, the provided '{split_option}' didn't seem to be numeric 1-4. Please try again.")
            time.sleep(2)

    if split_option == 5:
        print(f"\r\nYou've selected 'custom' splitting.")
        val = -1.0
        while val == -1.0:
            val = input(f"How much does the {OTHER_PERSON[who_paid]} owe? ($) ")
            try:
                val = val.split('$')[-1].strip()
                val = float(val)
                if val > amt or val < 0.0:
                    print(f"'{val}' is an invalid amount. Please try again.\r\n")
                    val = -1.0
                    continue
                val = round(val, 2)
            except:
                print(f"'{val}' is an invalid amount. Please try again.\r\n")
                time.sleep(2)
        amt = val
    print(f"Split option is: {OPTION_SPLITS[split_option - 1]}\r\n")
    return round(OPTION_MATH[split_option - 1] * amt, 2)

    
#############################################

def add_handler(base_url: str) -> bool:
    print("\r\nCool, let's **ADD** a transaction. We'll start by asking some questions about it...")
    time.sleep(2)

    transaction_name = get_valid_name("First, what NAME should we give this transaction?")
    account = which_account()
    person = who_paid()
    person_paid = get_valid_amount(f"Cool. How much did {person} pay?")
    other_person = how_to_split_transaction(person_paid, person)

    time.sleep(1)
    message = "Summary of transaction:\r\n\r\n"
    message += f"\tAccount: {account}\r\n"
    message += f"\tNamed: '{transaction_name}'\r\n"
    message += f"\t{person} paid ${person_paid}\r\n"
    message += f"\t{OTHER_PERSON[person]} now OWES ${other_person}"
    print(message)
    time.sleep(4)
    print("\r\n\r\n")

    transaction = {
        "item": transaction_name,
        "paid_by_name": person,
        "paid_amount": person_paid,
        "other_person_owes": other_person
    }
    db_table_name_list = account.lower().split(' ')
    db_table_name = '_'.join(db_table_name_list)
    handle_post(f"{base_url}/transactions/{db_table_name}", transaction)
        
    return True