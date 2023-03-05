from fastapi import FastAPI, Request, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from modules.backend import utils

# Crete app
app = FastAPI()

# Create templates
app.mount("/static", StaticFiles(directory="modules/static"), name="static")
templates = Jinja2Templates(directory="modules/static/templates")

# Home page
@app.get("/semillIAS_sing/home")
def home(request: Request):
    title = 'Demo app: Signs'
    return templates.TemplateResponse("home.html",{"request": request, "title": title})

# Page capture image
@app.get("/semillIAS_sing/upload_images")
def upload_images(request: Request):
    capture = 'Esperando imagen de la mano'
    return templates.TemplateResponse("capture.html", {"request": request, "title": capture})

@app.post("/semillIAS_sing/upload_images")
async def upload_images(request: Request, url_image: str = Form(...)):
    capture = 'Exitosa!'
    print(capture, type(url_image))
    utils.base64toimage(url_image)
    return templates.TemplateResponse("capture.html", {"request": request, "title": capture})