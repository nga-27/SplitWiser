""" API route(s) for making a payment / settling up an account """
from fastapi import APIRouter, HTTPException

from api.models.models import Payment
from api.libs.payments import make_payment, get_payments

router = APIRouter(
    prefix="/payments"
)

@router.get("/", tags=["Payment"], status_code=200)
def get_all_payments():
    """ Get all of the payments made by people """
    return get_payments()

@router.post("/", tags=["Payment"], status_code=201)
def post_new_payment(payment: Payment):
    """ Add a new payment to the DB, with necessary payment and transaction logic """
    code, msg = make_payment(payment)
    if code != 201:
        HTTPException(status_code=code, detail=msg)
    return msg
