from fastapi import APIRouter, HTTPException

from api.models.models import Payment
from api.libs.payments import make_payment

router = APIRouter(
    prefix="/payments"
)

@router.post("/", tags=["Payment"], status_code=201)
def post_new_payment(payment: Payment):
    code, msg = make_payment(payment)
    if code != 201:
        HTTPException(status_code=code, detail=msg)
    return msg
