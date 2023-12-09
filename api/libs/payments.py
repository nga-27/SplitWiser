import datetime
from typing import Dict, Tuple

from api.models.models import Payment, Transaction

from .db import post_to_db, get_db
from .summary import update_summary
from .utils import api_address_to_db_table, transaction_payers_and_debtors


def payment_as_payment(payment: Payment) -> None:
    payment.id = "0"
    add_payment = payment.dict()
    post_to_db(add_payment, 'Payment History')
    return


def payment_as_transaction(payment: Payment, db: dict):
    paid, owes = transaction_payers_and_debtors(
        payment, db['People']['__list__'], is_settle_up=True)
    
    transaction = Transaction(
        id="0",
        date=payment.date,
        item=f"PAYMENT on {payment.date}",
        paid_by_id=paid,
        owed_by_id=owes
    ).dict()
    post_to_db(transaction, api_address_to_db_table(payment.account))
    return


def handle_archival(payment: Payment, db: dict):
    account = api_address_to_db_table(payment.account)
    acc_transactions = db[account]
    print(acc_transactions)


def payment_to_account_handler(db: Dict[str, dict], payment: Payment) -> Tuple[int, str]:
    account = api_address_to_db_table(payment.account)
    payer = payment.payer
    debtor_amount = db['Summary'].get(account, {}).get(payer)
    if debtor_amount is None:
        return 404, f"'{payer}' or '{account}' not found as entered."
    
    if payment.amount > debtor_amount:
        return 400, f"Amount ${payment.amount} exceeds debt of {payer}, which is ${debtor_amount}."

    # Now we know the debt is okay to pay off!
    payment.date = datetime.datetime.now().strftime("%m/%d/%Y")
    payment_as_payment(payment)
    payment_as_transaction(payment, db)

    if payment.amount == debtor_amount:
        # Now we'll do the archiving!
        handle_archival(payment, db)
        return 201, "Payment and Settle Up was Successful"
    return 201, "Payment was Successful, but amount was less than a settle up amount."


############################################################

def make_payment(add_payment: Payment) -> Tuple[int, str]:
    full_db = get_db()
    code, msg = payment_to_account_handler(full_db, add_payment)
    update_summary()
    return code, msg