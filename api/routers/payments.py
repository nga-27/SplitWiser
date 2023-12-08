from fastapi import APIRouter

from api.models.models import Payment
from api.libs.payments import make_payment

router = APIRouter(
    prefix="/payments"
)

@router.post("/", tags=["Payment"], status_code=201)
def post_new_payment(payment: Payment):
    make_payment(payment)
    return "Payment Submitted"
