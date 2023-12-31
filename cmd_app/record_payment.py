""" record a payment / settle up handler for main cmd_app """
import time

from cmd_app.utils.api import handle_post, handle_get_payload
from cmd_app.utils.prompts import intro_and_choose_account, who_paid
from cmd_app.utils.ui import format_balances
from cmd_app.utils.constants import PrintColor


def get_balance_of_account(base_url: str, account: str, person: str) -> float:
    """get_balance_of_account

    Returns the balance of a particular account / table for a person

    Args:
        base_url (str): api base url
        account (str): account name
        person (str): person's name

    Returns:
        float: amount owed for a particular account by person
    """
    url = f"{base_url}/summary/"
    summary_data = handle_get_payload(url)
    modified_account_list = account.split('_')
    for i, word in enumerate(modified_account_list):
        modified_account_list[i] = word.capitalize()
        if word.capitalize() == 'And':
            modified_account_list[i] = 'and'
    modified_account = " ".join(modified_account_list)
    return summary_data[modified_account][person]


def post_payment(base_url: str, account: str, person: str, amount: float) -> None:
    """post_payment

    Posts the payment / settle up to the API

    Args:
        base_url (str): base url of the api
        account (str): account name
        person (str): person's name
        amount (float): amount made by the payment
    """
    payment = {
        "account": account,
        "payer": person,
        "amount": amount
    }
    handle_post(f"{base_url}/payments/", payment)


############################################

def record_handler(base_url: str) -> bool:
    """record_handler

    Handler to record a payment / settle an account

    Args:
        base_url (str): api base url

    Returns:
        bool: True to continue the main handler prompts
    """
    account, _ = intro_and_choose_account("Awesome. Let's record a payment.", is_for_payment=True)
    person = who_paid(is_settle_up_payment=True, color=PrintColor.BLUE)
    amount = get_balance_of_account(base_url, account, person)
    post_payment(base_url, account, person, amount)
    print(f"\r\n{PrintColor.BLUE}Payment was made successfully!{PrintColor.NORMAL}")
    time.sleep(1)

    balances = handle_get_payload(f"{base_url}/summary/")
    format_balances(balances)
    time.sleep(2)
    print("\r\n")
    return True
