from fastapi import APIRouter
from ..services.notes import testing

router = APIRouter(
    prefix="/notes",
    tags=["notes"]
)

@router.get("/")
def notes_check():
    return testing()