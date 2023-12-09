from fastapi import APIRouter

from api.libs.summary import get_all_summary, update_summary

router = APIRouter(
    prefix="/summary"
)

@router.get("/", tags=["Summary"])
def get_summary():
    update_summary()
    return get_all_summary()
