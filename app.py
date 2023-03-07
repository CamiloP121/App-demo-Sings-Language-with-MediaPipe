from fastapi import FastAPI, Request, File, UploadFile, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from modules.backend import utils, db
from pathlib import Path
import logging
from starlette.datastructures import URL

# Crete app
app = FastAPI()
logging.info('Starting App')

# Create directorys necessary
Path('temp').mkdir(parents=True, exist_ok=True)
Path('logs').mkdir(parents=True, exist_ok=True)

# Create database
db.create_db()

# Delete temporary files
for ext in ['*.jpg','*.txt', '*.pkl','*.json']:
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
    flag = utils.mp_apply(False)
    if flag: 
        redirect_url = URL(request.url_for('result')).include_query_params(msg="complete extraction")
        return RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
    else: 
        capture = '**Error** \nNo se encontro mano!'
        return templates.TemplateResponse("capture.html", {"request": request, "message": capture})

@app.get('/semillIAS_sing/result')
async def result(request: Request):
    results = utils.load_mp_results()
    return templates.TemplateResponse("result_capture.html", {"request": request, "orientation": results['orentation_hands'],
                                        "score": str(round(results['score'],3)*100)})


@app.post('/semillIAS_sing/result')
async def result(request: Request, h_hand:str = Form(...)):
    results = utils.load_mp_results()
    if h_hand == 'Si':
        print('Save results')
        db.insert_db(1,'test')
        return templates.TemplateResponse("result_capture.html", {"request": request, "orientation": results['orentation_hands'],
                                        "score": str(round(results['score'],3)*100), "message": 'La imagen sera cargada. !Muchas gracias por participar!'})
    elif h_hand == 'No':
        print('Return to upload image')
        redirect_url = URL(request.url_for('upload_images'))
        return RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
    else:
        return templates.TemplateResponse("result_capture.html", {"request": request, "orientation": results['orentation_hands'],
                                        "score": str(round(results['score'],3)*100)})

