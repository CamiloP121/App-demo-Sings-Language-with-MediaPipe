import base64
import numpy as np
from modules.backend.mediapipe import hands_detect
import cv2 as cv
import os
import json

def base64toimage(image_data: str, save:bool = True):
    '''
    Converts base64 to image
    ----------------------------------------------------------------
    Arg:
    img_data (str): base64 string
    save (bool, optional): whether to save the image or not. Defaults to True.
    Returns:
    imagae (Opcional)
    '''
    nparr = np.fromstring(base64.b64decode(image_data), np.uint8)
    image = cv.imdecode(nparr, cv.IMREAD_COLOR)
    if save:
        cv.imwrite('modules/static/temp/image.jpg', image)
        with open('modules/static/temp/image.txt', 'w') as file:
            file.write(image_data)
    else:
        return image
def mp_apply(plot:bool = True):
    '''
    Funcion use Mediapipe Google detected hands
    ----------------------------------------------------------------
    Arg:
    image (np.array): image
    plot (bool, optional): whether to plot the image or not. Defaults to True.
    '''
    if os.path.exists('modules/static/temp/image.jpg'):
        image = cv.imread('modules/static/temp/image.jpg')
        hands_detect(image, plot=False)
        if not os.path.exists('modules/static/temp/mp_results.json'): return False
        else: return True
    else: 
        return False
    
def load_mp_results():
    '''
    Load Mediapipe results
    ----------------------------------------------------------------
     Returns:
     mp_results (object): Mediapipe hands results
    '''
    with open('modules/static/temp/mp_results.json', 'r') as file:
        image_as_bytes = json.load(file)

    return image_as_bytes

def loadBase64toImage():
    '''
    Load image base64
    ----------------------------------------------------------------
     Returns:
     string image base64
    '''
    with open('modules/static/temp/image.txt', 'r') as file:
        img_data = file.read()
        Img = base64toimage(image_data= img_data, save=False)

    return Img

def live_video(cap):
    while True:
        ret, frame = cap.read()
        if ret:
            _, ima_draw = hands_detect(frame)
            flag, encodedImage = cv.imencode(".jpg", ima_draw)
            if not flag:
                continue
            yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                    bytearray(encodedImage) + b'\r\n')

if __name__ == '__main__':
    pass    
