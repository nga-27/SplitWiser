import time
from typing import Union

from cmd_app.utils.prompts import which_account, who_paid, get_numerical_valid_amount
from cmd_app.utils.api import handle_post
from cmd_app.utils.constants import OTHER_PERSON, PrintColor


def get_valid_name(message: str, color: Union[str, None] = None) -> str:
    print("")
    if color is None:
        color = PrintColor.NORMAL
    name2 = "N"
    while 'N' in name2:
        name = input(f"{message} ")
        check_name = f"Nice. Cool with '{color}{name}{PrintColor.NORMAL}'? "
        check_name += "(just hit enter if yes, or 'N' if to redo it.)"
        name2 = input(check_name).upper()
    return name


def how_to_split_transaction(amt: float, who_paid: str, color: Union[str, None] = None) -> float:
    """ returns what the other person pays """
    if color is None:
        color = PrintColor.NORMAL
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
    print(f"Split option is: {color}{OPTION_SPLITS[split_option - 1]}{PrintColor.NORMAL}\r\n")
    return round(OPTION_MATH[split_option - 1] * amt, 2)

    
#############################################

def add_handler(base_url: str) -> bool:
    msg = f"\r\nCool, let's {PrintColor.GREEN}**ADD**{PrintColor.NORMAL} "
    msg += "a transaction. We'll start by asking some questions about it..."
    print(msg)
    time.sleep(2)

    name_msg = f"First, what {PrintColor.GREEN}NAME{PrintColor.NORMAL} "
    name_msg += "should we give this transaction?"
    transaction_name = get_valid_name(name_msg, color=PrintColor.GREEN)
    account, color = which_account(is_for_payment=True)
    person = who_paid(color=PrintColor.GREEN)
    person_paid = get_numerical_valid_amount(
        f"Cool. How much did {person} pay?", color=PrintColor.GREEN)
    other_person = how_to_split_transaction(person_paid, person, color=PrintColor.GREEN)

    time.sleep(2)
    message = "Summary of transaction:\r\n\r\n"
    message += f"\tAccount: {color}{account}{PrintColor.NORMAL}\r\n"
    message += f"\tNamed: {PrintColor.BLUE}'{transaction_name}'{PrintColor.NORMAL}\r\n"
    message += f"\t{person} paid {PrintColor.GREEN}${person_paid}{PrintColor.NORMAL}\r\n"
    message += f"\t{OTHER_PERSON[person]} now OWES "
    message += f"{PrintColor.RED}${other_person}{PrintColor.NORMAL}"
    print(message)
    time.sleep(4)
    print("\r\n\r\n")

    transaction = {
        "item": transaction_name,
        "paid_by_name": person,
        "paid_amount": float(person_paid),
        "other_person_owes": float(other_person)
    }
    db_table_name_list = account.lower().split(' ')
    db_table_name = '_'.join(db_table_name_list)
    handle_post(f"{base_url}/transactions/{db_table_name}", transaction)

    return True
