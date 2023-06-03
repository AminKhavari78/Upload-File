import shutil, os
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=RedirectResponse)
def home():
    resp = RedirectResponse("/upload")
    return resp


@app.get("/upload", response_class=HTMLResponse)
async def upload(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/uploader")
async def create_upload_file(file: UploadFile = File(...)):
    upload_dir = os.path.join(os.getcwd(), "uploads")
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    destination = os.path.join(upload_dir, file.filename)
    with open(destination, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": file.filename}




