import datetime

from fastapi import APIRouter

from api.models.models import AddTransaction
from api.libs.transactions import add_transaction, get_all_transactions

router = APIRouter(
    prefix="/transactions"
)


@router.get("/jill_and_nick", tags=["Transaction"], status_code=200)
def get_jill_and_nick_transactions() -> dict:
    return get_all_transactions('Jill and Nick')

@router.get("/house_avery", tags=["Transaction"], status_code=200)
def get_jill_and_nick_transactions() -> dict:
    return get_all_transactions('House Avery')

@router.post("/house_avery", tags=["Transaction"], status_code=201)
def post_new_house_avery_transaction(add_trans: AddTransaction):
    add_transaction(add_trans, 'House Avery')
    return "Transaction Submitted"

@router.post("/jill_and_nick", tags=["Transaction"], status_code=201)
def post_new_jill_and_nick_transaction(add_trans: AddTransaction):
    add_transaction(add_trans, 'Jill and Nick')
    return "Transaction Submitted"