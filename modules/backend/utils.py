import base64
import numpy as np
from modules.backend.mediapipe import hands_detect
import cv2 as cv
import os

def base64toimage(img_data: str, save:bool = True):
    '''
    Converts base64 to image
    ----------------------------------------------------------------
    Arg:
    img_data (str): base64 string
    save (bool, optional): whether to save the image or not. Defaults to True.
    '''
    image_as_bytes = str.encode(img_data)  # convert string to bytes
    image = base64.b64decode(image_as_bytes)
    if save:
        with open('modules/static/temp/image.jpg', 'wb') as file:
            file.write(image)

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
        hands_detect(image, plot=plot)
        if not os.path.exists('modules/static/temp/mp_results.pkl'): return False
        else: return True
    else: 
        return False


if __name__ == '__main__':
    pass    
