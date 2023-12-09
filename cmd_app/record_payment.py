import datetime

from cmd_app.utils.api import handle_post
from cmd_app.utils.prompts import intro_and_choose_account, who_paid, get_numerical_valid_amount

def account_logic_handler():
    # logic if we archive entries or not
    print("")


def post_payment(base_url: str, account: str, person: str, amount: float) -> None:
    payment = {
        "account": account,
        "payer": person,
        "amount": amount
    }
    handle_post(f"{base_url}/payments/", payment)


############################################

def record_handler(base_url: str) -> bool:
    account = intro_and_choose_account("Awesome. Let's record a payment.")
    person = who_paid(is_settle_up_payment=True)
    amount = get_numerical_valid_amount(f"Cool. How much did {person} pay?")
    post_payment(base_url, account, person, amount)
    return True
