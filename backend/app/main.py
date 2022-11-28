from fastapi import FastAPI
from .routers import book, notes, sign

from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

app.include_router(book.router)
app.include_router(notes.router)
app.include_router(sign.router)

@app.get("/")
def root_check():
    return {"status": "OK", "message": "Welcome to SpeakUp Rest API."}