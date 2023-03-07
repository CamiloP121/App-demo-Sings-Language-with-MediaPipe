import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import mediapipe as mp
import dill

def plot_image(image:np.ndarray,name_window:str):
    '''
    Plot image
    ----------------------------------------------------------------
    Args:
    image (np.ndarray): image to plot
    name_window (str): window name
    '''
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
    plot (bool): if True, plot the image
    Returns:
    flag (bool): if True, detect hands in image
    '''
    # Crate mp-hands model detection
    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands
    
    # Image original -> image
    if plot:
        plot_image(image,name_window='original image')

    # Image draw results -> image_dw
    ## Flip image and copy
    image_dw = image.copy()
    image_dw = cv.flip(image_dw, 1)
    lb = 'No se detecta mano'
    with mp_hands.Hands(
      static_image_mode=False,
      max_num_hands=1,
      min_detection_confidence=0.5) as hands:
      # DImnesiones (Relebant for the extraction of stitches)
      height, width, _ = image.shape
      # Convert to RGB, neceesary for MediaPipe
      frame_rgb = cv.cvtColor(image_dw, cv.COLOR_BGR2RGB)
      # Model results
      results = hands.process(frame_rgb)
      if results.multi_hand_landmarks is not None:
        lb = 'Se detecto mano'
        # Draw hands
        if plot:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                        image_dw, hand_landmarks, mp_hands.HAND_CONNECTIONS,mp_drawing.DrawingSpec(color=(255,255,0)))
            plot_image(image_dw, name_window='Result MediaPipe')

        with open('temp/mp_results.pkl', 'wb') as file:
           dill.dump(results, file)
    print(lb)


    


