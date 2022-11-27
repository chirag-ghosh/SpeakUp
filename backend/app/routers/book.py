from fastapi import APIRouter
from ..services.book import testing

router = APIRouter(
    prefix="/book",
    tags=["book"]
)

@router.get("/")
def book_check():
    return testing()