from api.models.models import Payment
from .db import post_to_db


def make_payment(add_payment: Payment) -> None:
    payment = add_payment.dict()
    payment['id'] = "0"
    post_to_db(payment, 'Payment History')
    return