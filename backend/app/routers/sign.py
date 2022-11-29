import base64
from fastapi import APIRouter
from ..services.sign import testing, getSignVideo

router = APIRouter(
    prefix="/sign",
    tags=["sign"]
)

@router.get("/")
def sign_check():
    return testing()

@router.get("/video")
def sign_video(url:str):
    videoPath = getSignVideo(url)
    with open(videoPath, 'rb') as videoFile:
        encoded_file = base64.b64encode(videoFile.read())
    return {'video':encoded_file.decode('utf-8', errors='replace')}