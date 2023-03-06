import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import mediapipe as mp

def plot_image(image:np.ndarray,name_window:str):
    '''
    Plot image
    ----------------------------------------------------------------
    Args:
    image (np.ndarray): image to plot
    name_window (str): window name
    '''
    plt.imshow(image)
    plt.show()
    # show the image, provide window name first
    cv.imshow(name_window, image)
    # add wait key. window waits until user presses a key
    cv.waitKey(0)
    # and finally destroy/close all open windows
    cv.destroyAllWindows()
    
def hands_detect(image:np.ndarray,plot:bool):
    '''
    Detect hands in image
    ----------------------------------------------------------------
    Args:
    image (np.ndarray): image to detect hands in
    '''
    # Crate mp-hands model detection
    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands.Hands()
    
    if plot:
        plot_image(image,name_window='original image')

    


