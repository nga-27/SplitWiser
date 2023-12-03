import datetime

from fastapi import APIRouter

from api.models.models import Transaction, AddTransaction
from api.libs.db import add_transaction, get_all_transactions

router = APIRouter(
    prefix="/transactions"
)


@router.get("/jill_and_nick", tags=["Transaction"], status_code=200)
def get_jill_and_nick_transactions():
    return get_all_transactions('Jill and Nick')

@router.get("/house_avery", tags=["Transaction"], status_code=200)
def get_jill_and_nick_transactions():
    return get_all_transactions('House Avery')

@router.post("/house_avery", tags=["Transaction"], status_code=201)
def post_new_house_avery_transaction(add_trans: AddTransaction):
    print(add_trans)
    # trans = Transaction(
    #     date=datetime.datetime.now().strftime("%m/%d/%Y"),
    #     )
    return "Transaction Submitted"