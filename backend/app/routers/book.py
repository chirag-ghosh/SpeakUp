from fastapi import APIRouter

router = APIRouter(
    prefix="/book",
    tags=["book"]
)

@router.get("/")
def book_check():
    return {"message": "This is Book endpoint."}