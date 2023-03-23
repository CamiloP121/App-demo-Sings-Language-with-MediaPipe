from fastapi import FastAPI, Request, File, UploadFile, Form, status, WebSocket
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from modules.backend import utils, db
import asyncio
from pathlib import Path
import logging
from starlette.datastructures import URL
from modules.backend.mediapipe import hands_detect
import cv2
import base64

import warnings
warnings.filterwarnings("ignore")

# Crete app
app = FastAPI()
logging.info('Starting App')

# Create directorys necessary
Path('temp').mkdir(parents=True, exist_ok=True)
Path('logs').mkdir(parents=True, exist_ok=True)
Path('modules/backend/db').mkdir(parents=True, exist_ok=True)

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
    title = '¡Lenguaje de señas para todos!'
    return templates.TemplateResponse("home.html",{"request": request, "title": title})

# Page capture image
@app.get("/semillIAS_sing/upload_images")
def upload_images(request: Request):
    title = 'Adquisición de nuevas imagenes'
    return templates.TemplateResponse("capture.html", {"request": request, 'title':title})

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
        capture = '**Error** ¡No se encontró mano! Vuelve a intentarlo'
        return templates.TemplateResponse("capture.html", {"request": request, "message": capture})

@app.get('/semillIAS_sing/result')
async def result(request: Request):
    results = utils.load_mp_results()
    title = 'Resultado de adqusición'
    return templates.TemplateResponse("result_capture.html", {"request": request,'title':title , "orientation": results['orentation_hands'],
                                        "score": str(round(float(results['score'])*100,3))})


@app.post('/semillIAS_sing/result')
async def result(request: Request, h_hand:str = Form(...)):
    results = utils.load_mp_results()
    if h_hand == 'Si':
        try:
            image_b64 = utils.imageBase64()
            results['image'] = image_b64
            db.insert_db(results)
            title = 'Resultado de adquisición'
            return templates.TemplateResponse("result_capture.html", {"request": request, 'title':title ,"orientation": results['orentation_hands'],
                                        "score": str(round(float(results['score'])*100,3)), "message": 'La imagen será cargada. !Muchas gracias por participar!'})
        
        except Exception as e:
            print(e)
            title = 'Resultado de adquisición (Error)'
            return templates.TemplateResponse("result_capture.html", {"request": request,'title':title, "orientation": results['orentation_hands'],
                                        "score": str(round(float(results['score'])*100,3)), "message_raise": 'Error en la carga de datos, intentelo de nuevo'})
    elif h_hand == 'No':
        print('Return to upload image')
        redirect_url = URL(request.url_for('upload_images'))
        return RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
    else:
        title = 'Resultado de adqusición'
        return templates.TemplateResponse("result_capture.html", {"request": request,'title':title ,"orientation": results['orentation_hands'],
                                        "score": str(round(float(results['score'])*100,3))})

@app.route("/semillIAS_sing/database_resume")
def database_resume(request:Request):
    df,_ = db.download_db()

    tables=[df.to_html(classes='data')]
    titles=df.columns.values
    header = True
    return templates.TemplateResponse("db_resume.html", {"request": request,"tables": tables, "titles": titles})


@app.route("/semillIAS_sing/predict")
def predict(request:Request):
    title = 'Predicción alfabeto de Señas'
    return templates.TemplateResponse("predict.html", {"request": request, 'title':title})


async def capture_video(websocket: WebSocket):
    '''
    Captures video and processes it Mediapipe
    ----------------------------------------------------------------
    Args:
    Websocket: WebSocket (Video text)
    Returns:
    Video procesed
    '''
    while True:
        # Capturar un cuadro de video de la cámara web
        data = await websocket.receive_text()
        # Decodificar los datos de la imagen en base64
        img = utils.base64toimage(data.split(',')[1].encode(), save=False)
        # Procesar el cuadro de video
        _ , img, _ = hands_detect(img, plot=False, on_predictions=True)
        img = cv2.flip(img, 1)
        _, buffer = cv2.imencode('.jpg', img)
        processed_frame =  base64.b64encode(buffer).decode("ascii")

        # Enviar el cuadro de video procesado a través del socket
        await websocket.send_text(processed_frame)


@app.websocket('/semillIAS_sing/predict/ws')
async def websocket_endpoint(websocket: WebSocket):
    # Abrir la conexión del socket
    print('Ws conections...')
    await websocket.accept()
    try:
        # Iniciar la captura de video desde la cámara web y enviar cada cuadro procesado a través del socket
        await capture_video(websocket)
    finally:
        # Cerrar la conexión del socket cuando se cierra la conexión
        await websocket.close()        
        
    

