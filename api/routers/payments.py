from fastapi import APIRouter, HTTPException

from api.models.models import Payment
from api.libs.payments import make_payment

router = APIRouter(
    prefix="/payments"
)


@router.post("/jill_and_nick", tags=["Payment"], status_code=201)
def post_new_jill_and_nick_transaction(payment: Payment):
    make_payment(payment)
    return "Payment Submitted"
