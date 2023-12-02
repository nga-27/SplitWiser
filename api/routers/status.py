from fastapi import APIRouter

from api.libs.status import get_all_status

router = APIRouter(
    prefix="/status"
)


@router.get("/", tags=["Status"])
def get_status():
    return get_all_status()