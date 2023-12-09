import time

from cmd_app.utils.api import handle_post, handle_get_payload
from cmd_app.utils.prompts import intro_and_choose_account, who_paid


def get_balance_of_account(base_url: str, account: str, person: str) -> float:
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
    payment = {
        "account": account,
        "payer": person,
        "amount": amount
    }
    handle_post(f"{base_url}/payments/", payment)


############################################

def record_handler(base_url: str) -> bool:
    account = intro_and_choose_account("Awesome. Let's record a payment.", is_for_payment=True)
    person = who_paid(is_settle_up_payment=True)
    amount = get_balance_of_account(base_url, account, person)
    post_payment(base_url, account, person, amount)
    print("\r\nPayment was made successfully!")
    time.sleep(2)
    print("\r\n")
    return True
