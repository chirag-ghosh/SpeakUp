from fastapi import APIRouter
from ..services.sign import testing

router = APIRouter(
    prefix="/sign",
    tags=["sign"]
)

@router.get("/")
def sign_check():
    return testing()