""" Payment logic handlers """
import datetime
from typing import Dict, Tuple

from api.models.models import Payment, Transaction

from .db import post_to_db, get_db, patch_entire_table
from .summary import update_summary
from .utils import api_address_to_db_table, transaction_payers_and_debtors


def payment_as_payment(payment: Payment) -> None:
    """payment_as_payment

    To record the payment on the payment ledger, we need to record it as a payment as well

    Args:
        payment (Payment): payment object from FastAPI
    """
    payment.id = "0"
    add_payment = payment.dict()
    post_to_db(add_payment, 'Payment History')


def payment_as_transaction(payment: Payment, _db: dict):
    """payment_as_transaction

    To record the payment on the ledger, we need to record it as a transaction (first step)

    Args:
        payment (Payment): payment object from FastAPI
        _db (dict): json db snapshot, top-level keys are table names
    """
    paid, owes = transaction_payers_and_debtors(
        payment, _db['People']['__list__'], is_settle_up=True)

    transaction = Transaction(
        id="0",
        date=payment.date,
        item=f"PAYMENT on {payment.date}",
        paid_by_id=paid,
        owed_by_id=owes
    ).dict()
    post_to_db(transaction, api_address_to_db_table(payment.account))


def handle_archival(payment: Payment) -> None:
    """handle_archival

    On a payment of the exact amount, archive the older transactions to the 'Archive' account

    Args:
        payment (Payment): payment record object from fastAPI
    """
    account = api_address_to_db_table(payment.account)
    acc_transactions = get_db()[account]
    archival_name = f"Archived - {account}"
    for i in range(len(acc_transactions) - 1, -1, -1):
        transaction = acc_transactions[str(i)]
        post_to_db(transaction, archival_name)
    patch_entire_table({}, account)


def payment_to_account_handler(_db: Dict[str, dict], payment: Payment) -> Tuple[int, str]:
    """payment_to_account_handler

    Major piece of the logic to make sure the payment object is valid. Some cases it handles:
        - payment made was < $0
        - account or person wasn't available
        - payment made was > actual debt of that amount
        - if the payment made was < the actual debt of the person (and not to clear other
        transactions)
        - if payment was the exact amount, to record the payment and then settle up the account

    Args:
        _db (Dict[str, dict]): entire db, table names as top-level keys
        payment (Payment): payment record object from FastAPI

    Returns:
        Tuple[int, str]: status code, status message (if something didn't work properly)
    """
    account = api_address_to_db_table(payment.account)
    payer = payment.payer
    debtor_amount = _db['Summary'].get(account, {}).get(payer)
    if debtor_amount is None:
        return 404, f"'{payer}' or '{account}' not found as entered."

    if payment.amount > debtor_amount:
        return 400, f"Amount ${payment.amount} exceeds debt of {payer}, which is ${debtor_amount}."

    if payment.amount <= 0.0 and debtor_amount != 0.0:
        # In the case where transactions have canceled in an account, we still want it off the books
        # so we'll record it anyway if the amount is $0
        return 400, f"Amount ${payment.amount} is not valid."

    # Now we know the debt is okay to pay off!
    payment.date = datetime.datetime.now().strftime("%m/%d/%Y")
    payment_as_payment(payment)
    payment_as_transaction(payment, _db)

    if payment.amount == debtor_amount:
        # Now we'll do the archiving!
        handle_archival(payment)
        return 201, "Payment and Settle Up was Successful"
    return 201, "Payment was Successful, but amount was less than a settle up amount."


############################################################


def get_payments() -> dict:
    """get_payments

    Get the records of payments

    Returns:
        dict: payment data as a json object
    """
    payment_db = get_db()['Payment History']
    return payment_db


def make_payment(add_payment: Payment) -> Tuple[int, str]:
    """make_payment

    Top-level function that runs all payment and settle up logic

    Args:
        add_payment (Payment): Payment object from the API that will be the payment record

    Returns:
        Tuple[int, str]: "api" status code, status message (if something failed or wasn't ok)
    """
    full_db = get_db()
    code, msg = payment_to_account_handler(full_db, add_payment)
    update_summary()
    return code, msg
