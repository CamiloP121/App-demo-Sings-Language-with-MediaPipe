from fastapi import FastAPI, Request, File, UploadFile, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from modules.backend import utils
from pathlib import Path
import logging
from starlette.datastructures import URL

# Crete app
app = FastAPI()
logging.info('Starting App')

# Create directorys necessary
Path('temp').mkdir(parents=True, exist_ok=True)
Path('logs').mkdir(parents=True, exist_ok=True)

# Delete temporary files
for ext in ['*.jpg','*.txt', '*.pkl']:
    for file in Path('modules/static/temp').glob(ext):
        file.unlink()

# Configure logging

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
    return templates.TemplateResponse("capture.html", {"request": request})

@app.post("/semillIAS_sing/upload_images")
async def upload_images(request: Request, url_image: str = Form(...)):
    # Load image
    utils.base64toimage(url_image.split(',')[1])
    # Mp detect hands
    flag = utils.mp_apply()
    if flag: 
        redirect_url = URL(request.url_for('result')).include_query_params(msg="")
        return RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
    else: 
        capture = '**Error** \nNo se encontro mano!'
        return templates.TemplateResponse("capture.html", {"request": request, "mensagge": capture})

@app.get('/semillIAS_sing/result')
async def result(request: Request):
    return templates.TemplateResponse("result_capture.html", {"request": request})

