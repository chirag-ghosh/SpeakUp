import base64
from fastapi import APIRouter

from backend.app.services.notes import testing

from ..services.braille import url_to_braille, testing

router = APIRouter(
    prefix="/notes",
    tags=["notes"]
)

@router.get("/")
def braille_check():
    return testing()

@router.get("/braille")
def get_barille(url:str):
    braille_text = url_to_braille(url)
    if braille_text is None:
        return {}
    return braille_text