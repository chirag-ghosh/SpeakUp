from fastapi import APIRouter

router = APIRouter(
    prefix="/notes",
    tags=["notes"]
)

@router.get("/")
def notes_check():
    return {"message": "This is Notes endpoint."}