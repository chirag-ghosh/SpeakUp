from fastapi import APIRouter

router = APIRouter(
    prefix="/sign",
    tags=["sign"]
)

@router.get("/")
def sign_check():
    return {"message": "This is Sign Language endpoint."}