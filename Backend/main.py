from fastapi import FastAPI, Form
from fastapi.responses import FileResponse, RedirectResponse

from database import create_database
from services.shorten_logic import shorten_url, get_original_url

app = FastAPI()

@app.get("/")
def home():
    return FileResponse("../Frontend/index.html")


@app.post("/shorten")
def shorten(url: str = Form(...)):
    code = shorten_url(url)
    print(f"Shortened url - http://127.0.0.1:8000/{code}")
    
    return {"short_url": f"http://127.0.0.1:8000/{code}"}


@app.get("/{short_code}")
def original_url(short_code):
    original_url = get_original_url(short_code)
    if original_url is None:
        return {
            "error": "Short URL not found"
        }

    print(f"Opened URL - {original_url}")
    return RedirectResponse(
        url=original_url,
        status_code=302
    )
