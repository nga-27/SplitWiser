from fastapi import APIRouter, HTTPException

from api.models.models import AddTransaction
from api.libs.transactions import (
    add_transaction, get_transactions, delete_transaction
)

router = APIRouter(
    prefix="/transactions"
)


@router.get("/jill_and_nick", tags=["Transaction"], status_code=200)
def get_jill_and_nick_transactions() -> dict:
    return get_transactions('Jill and Nick')

@router.get("/house_avery", tags=["Transaction"], status_code=200)
def get_house_avery_transactions() -> dict:
    return get_transactions('House Avery')

@router.post("/house_avery", tags=["Transaction"], status_code=201)
def post_new_house_avery_transaction(add_trans: AddTransaction):
    add_transaction(add_trans, 'House Avery')
    return "Transaction Submitted"

@router.post("/jill_and_nick", tags=["Transaction"], status_code=201)
def post_new_jill_and_nick_transaction(add_trans: AddTransaction):
    add_transaction(add_trans, 'Jill and Nick')
    return "Transaction Submitted"

@router.get("/house_avery/{id}", tags=["Transaction"], status_code=200)
def get_house_avery_transaction(id: int) -> dict:
    transaction = get_transactions('House Avery', str(id))
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction Not Found")
    return transaction

@router.get("/jill_and_nick/{id}", tags=["Transaction"], status_code=200)
def get_jill_and_avery_transaction(id: int) -> dict:
    transaction = get_transactions('Jill and Nick', str(id))
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction Not Found")
    return transaction

@router.delete("/house_avery/{id}", tags=["Transaction"], status_code=201)
def delete_house_avery_transaction(id: str):
    res = delete_transaction(id, 'Jill and Nick')
    if res is None:
        raise HTTPException(status_code=404, detail=f"Transaction with id #{id} not found.")
    return res

@router.delete("/jill_and_nick/{id}", tags=["Transaction"], status_code=201)
def delete_jill_and_nick_transaction(id: str) -> dict:
    res = delete_transaction(id, 'Jill and Nick')
    if res is None:
        raise HTTPException(status_code=404, detail=f"Transaction with id #{id} not found.")
    return res

#########################################################

@router.get("/archived/jill_and_nick", tags=["Transaction"], status_code=200)
def get_archived_jill_and_nick_transactions() -> dict:
    return get_transactions('Archived - Jill and Nick')

@router.get("/archived/house_avery", tags=["Transaction"], status_code=200)
def get_archived_house_avery_transactions() -> dict:
    return get_transactions('Archived - House Avery')
