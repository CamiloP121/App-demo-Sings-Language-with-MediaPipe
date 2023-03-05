from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Crete app
app = FastAPI()

# Create templates
app.mount("/static", StaticFiles(directory="modules/static"), name="static")
templates = Jinja2Templates(directory="modules/static/templates")

@app.get("/semillIAS_sing/{id}", response_class=HTMLResponse)
async def home(request: Request, id:str):
    if id == 'home':
        title = 'Demo app: Signs'
        return templates.TemplateResponse("home.html",{"request": request, "title": title})


@app.post("/semillIAS_sing/upload_images")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}