""" API Route(s) for summaries / overall balances among accounts """
from fastapi import APIRouter

from api.libs.summary import get_all_summary, update_summary

router = APIRouter(
    prefix="/summary"
)

@router.get("/", tags=["Summary"])
def get_summary():
    """ Return the balances and summary of all active (non-archival) accounts """
    update_summary()
    return get_all_summary()
