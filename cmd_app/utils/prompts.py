""" Command prompts for main application """
import time
from typing import Tuple, Union

from .constants import ACCOUNTS, PrintColor


def which_account(is_for_payment: bool = False) -> Tuple[str, str]:
    """which_account

    Prompts to get the user to enter in the correct account

    Args:
        is_for_payment (bool, optional): flag to hide 'Archived' accounts. Defaults to False.

    Returns:
        Tuple[str, str]: Account name, Account "color" as a special string
    """
    colors = (PrintColor.GREEN, PrintColor.MAGENTA, PrintColor.CYAN, PrintColor.BLUE)
    name = 0
    accounts = list(ACCOUNTS)
    if is_for_payment:
        accounts = accounts[0:2]
    end_of_options = len(accounts)
    acc_colors = {item: colors[i] for i, item in enumerate(accounts)}

    while name not in (range(1, len(accounts) + 1)):
        acc_options = ""
        for i, item in enumerate(accounts):
            acc_options += f"\r\n\t{i+1}. {acc_colors[item]}{item}{PrintColor.NORMAL}"
        options = f"\r\nAccounts:{acc_options}"
        print(options)
        name = input(f"\r\nAlright, which account should we use? (1-{end_of_options}) ").strip()
        try:
            name = int(name)
            if name not in (range(1, len(accounts) + 1)):
                name = 0
                msg = f"\r\nSorry, that didn't seem to be 1-{end_of_options}. Please try again.\r\n"
                print(msg)
                time.sleep(2)
        except: # pylint: disable=bare-except
            name = 0
            print(f"\r\nSorry, that didn't seem to be 1-{end_of_options}. Please try again.\r\n")
            time.sleep(2)
    msg = "Nice. You've chosen account "
    msg += f"'{acc_colors[accounts[name - 1]]}{accounts[name - 1]}{PrintColor.NORMAL}'."
    print(msg)
    time.sleep(2)
    return ACCOUNTS[name - 1], acc_colors[accounts[name - 1]]


def intro_and_choose_account(message: str, is_for_payment: bool = False) -> Tuple[str, str]:
    """intro_and_choose_account

    Prompts to introduce an action and have the user select the account to operate upon

    Args:
        message (str): Opening introductory message
        is_for_payment (bool, optional): Flag to hide 'Archived' accounts. Defaults to False.

    Returns:
        Tuple[str, str]: account url (for api), color of account for printing
    """
    print(f"\r\n{message}")
    time.sleep(1)
    account, color = which_account(is_for_payment=is_for_payment)
    account_list = account.lower().split(' ')
    account_url = '_'.join(account_list)
    if '-' in account_list:
        account_url = f"{account_list[0]}/{account_list[2]}_{account_list[3]}"
        if len(account_list) > 4:
            account_url += f"_{account_list[4]}"
    return account_url, color


def input_id_handler(id_str: str, num_transactions: int) -> str:
    """input_id_handler

    Prompts to get a row id of a transaction entered correctly

    Args:
        id_str (str): attempted id (or 'menu')
        num_transactions (int): number of available transactions, as a safeguard check

    Returns:
        str: correct id or "" on a bad option
    """
    id_str = id_str.strip()
    if 'menu' in id_str.lower():
        return 'menu'
    try:
        id_ = int(id_str)
        if id_ > num_transactions - 1 or id_ < 0:
            print(f"'{id_}' is not in range of 0 - {num_transactions - 1}. Please try again.\r\n")
            time.sleep(1)
            return ""
    except: # pylint: disable=bare-except
        msg = f"'{id_}' is not a valid number in range of 0 - {num_transactions - 1}. "
        msg += "Please try again.\r\n"
        print(msg)
        time.sleep(1)
        return ""
    return str(id_)


def who_paid(is_settle_up_payment: bool = False, color: Union[str, None] = None) -> str:
    """who_paid

    Prompts to configure who paid for a transaction or settle up payment

    Args:
        is_settle_up_payment (bool, optional): flag for settle up payments. Defaults to False.
        color (Union[str, None], optional): special string for account printing. Defaults to None.

    Returns:
        str: person's name referencing a DB entry
    """
    if color is None:
        color = PrintColor.NORMAL
    print("")
    okay_for_transaction = False
    first_input = 'made this payment' if is_settle_up_payment else 'paid for this transaction'
    second_input = 'making this payment' if is_settle_up_payment else 'paying for this'
    while not okay_for_transaction:
        person = ""
        while person not in ('Jill', 'Nick'):
            person = input(f"Who {first_input}? (Jill or Nick) ")
            if 'jill' not in person.lower() and 'nick' not in person.lower():
                print("Hmmm. That didn't look like 'Jill' or 'Nick'. Please try again.\r\n")
                person = ""
                time.sleep(2)
                continue
            if 'jill' in person.lower():
                person = 'Jill'
            else:
                person = 'Nick'

        msg = f"Cool. Are you good with '{color}{person}{PrintColor.NORMAL}' "
        msg += f"{second_input}? (hit enter if yes) "
        is_fine = input(msg)
        if is_fine in ('', 'yes'):
            okay_for_transaction = True
    return person


def get_numerical_valid_amount(message: str, color: Union[str, None] = None) -> float:
    """get_numerical_valid_amount

    Prompts and checks to ensure a valid amount value is entered by the user

    Args:
        message (str): input prompt to the user
        color (Union[str, None], optional): special string for colors. Defaults to None.

    Returns:
        float: valid amount that could be a cost figure
    """
    if color is None:
        color = PrintColor.NORMAL
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
            msg = "I'm sorry, that didn't seem to be a valid amount. "
            msg += "Try in the form of XXX.YY or XXX."
            print(msg)
            time.sleep(2)
            continue

        msg = f"Are you happy with the amount of {color}${amt}{PrintColor.NORMAL}? "
        msg += "(enter or 'yes') "
        verify = input(msg)
        if verify != '' and verify.strip().lower() != 'yes':
            amt = -1.0
    return amt
