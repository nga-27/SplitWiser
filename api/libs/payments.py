from typing import Dict

from api.models.models import Payment

from .db import post_to_db, get_db
from .summary import update_summary


def payment_to_account_handler(db: Dict[str, dict], payment: Payment):
    print(db['Summary'])

def make_payment(add_payment: Payment) -> None:
    full_db = get_db()
    payment = add_payment.dict()
    payment['id'] = "0"
    # post_to_db(payment, 'Payment History')
    # update_summary()
    return