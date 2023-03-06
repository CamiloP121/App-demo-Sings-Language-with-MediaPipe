import base64
import numpy as np
from modules.backend.mediapipe import hands_detect

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
        with open('temp/image.jpg', 'wb') as file:
            file.write(image)

    return image

def mp_apply(image:np.array, plot:bool = True):
    '''
    Funcion use Mediapipe Google detected hands
    ----------------------------------------------------------------
    Arg:
    image (np.array): image
    plot (bool, optional): whether to plot the image or not. Defaults to True.
    '''
    hands_detect(image, plot=plot)

if __name__ == '__main__':
    pass    
