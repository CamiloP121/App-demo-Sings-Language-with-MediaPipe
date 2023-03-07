import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import mediapipe as mp
import json
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

def check_hands_points(x_points:float, y_points:float):
   ''' 
   Check all hands points exist and stay in the images. x_points and y_points < 1.0
   ----------------------------------------------------------------
   Args:
   x_points: float
   y_points: float
   Returns:
   True if all hands points in the image
   False if all hands points not in the image
   '''
   if x_points > 1.0 or y_points > 1.0:
      return False
   if x_points < -1.0 or y_points < -1.0:
      return False
   return True

def extract_hand_points(results:object):
   '''
   Extract all hands points
   ----------------------------------------------------------------
   Args:
   results (object): Object results mediapipe
   Returns:
   hand_points (dict): dict of hands points and other characteristics
   '''
   dic_results = {}
   for hand_landmarks,hand_label in zip(results.multi_hand_landmarks,results.multi_handedness):
    labels = 'WRIST;THUMB_CMC;THUMB_MCP;THUMB_IP;THUMB_TIP;INDEX_FINGER_MCP;INDEX_FINGER_PIP;INDEX_FINGER_DIP;INDEX_FINGER_TIP;MIDDLE_FINGER_MCP;MIDDLE_FINGER_PIP;MIDDLE_FINGER_DIP;MIDDLE_FINGER_TIP;RING_FINGER_MCP;RING_FINGER_PIP;RING_FINGER_DIP;RING_FINGER_TIP;PINKY_MCP;PINKY_PIP;PINKY_DIP;PINKY_TIP'
    
    for lb, points in zip(labels.split(';'), hand_landmarks.landmark):
        if check_hands_points(points.x, points.y):
           dic_results[lb] = [round(points.x,4),round(points.y,4),round(points.z,4)]
        else: return np.nan, False

    if hand_label.classification[0].label == 'Left': or_hand = 'Izquierda'
    else: or_hand = 'Derecha'
    dic_results['score'] = round(hand_label.classification[0].score,4)
    dic_results['orentation_hands'] = or_hand
    
    print('-> Complete extraction')
    return dic_results, True

    
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

        # Extract results
        dic_result, flag = extract_hand_points(results)
        # Save results
        if flag:
            with open('modules/static/temp/mp_results.json', 'w') as f:
                json.dump(dic_result, f, indent=2)
            with open('test/mp_results.json', 'w') as f:
                json.dump(dic_result, f, indent=2)

        # Draw hands
    
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                    image_dw, hand_landmarks, mp_hands.HAND_CONNECTIONS,mp_drawing.DrawingSpec(color=(255,255,0)))
        # Save drawings mp
        cv.imwrite('modules/static/temp/image_mp.jpg', image_dw)
        if plot:
            plot_image(image_dw, name_window='Result MediaPipe')
        
    print(lb)


    


