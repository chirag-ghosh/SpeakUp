import base64
from fastapi import APIRouter
from fastapi.responses import FileResponse

from ..services.notes import note_make, testing

router = APIRouter(
    prefix="/notes",
    tags=["notes"]
)

@router.get("/")
def notes_check():
    return testing()

@router.get("/image")
def img_to_bb():
    img_src = note_make(just_img=True)
    if img_src is None:
        return {}
    response = FileResponse(img_src)
    return response

@router.get("/audio")
def note_to_audio(url:str):
    audio_path = note_make(url)
    if audio_path is None:
        return {}
    with open(audio_path, 'rb') as audio_file:
        encoded_file = base64.b64encode(audio_file.read())
    image_path = note_make(just_img=True)
    return {'audio':encoded_file.decode('utf-8', errors='replace'), 'image':image_path}
