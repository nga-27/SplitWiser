import datetime
from typing import Dict, Tuple

from api.models.models import Payment, Transaction

from .db import post_to_db, get_db
from .summary import update_summary
from .utils import api_address_to_db_table


def payment_to_account_handler(db: Dict[str, dict], payment: Payment) -> Tuple[int, str]:
    account = api_address_to_db_table(payment.account)
    payer = payment.payer
    debtor_amount = db['Summary'].get(account, {}).get(payer)
    if debtor_amount is None:
        return 404, f"'{payer}' or '{account}' not found as entered."
    
    if payment.amount > debtor_amount:
        return 400, f"Amount ${payment.amount} exceeds debt of {payer}, which is ${debtor_amount}."
    # Now we know the debt is okay to pay off!

def make_payment(add_payment: Payment) -> None:
    full_db = get_db()
    code, msg = payment_to_account_handler(full_db, add_payment)
    print(f"{code} --> {msg}")
    payment = add_payment.dict()
    payment['date'] = datetime.datetime.now().strftime("%m/%d/%Y")
    payment['id'] = "0"
    # post_to_db(payment, 'Payment History')
    # update_summary()
    return