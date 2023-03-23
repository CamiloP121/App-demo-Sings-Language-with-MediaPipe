import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import mediapipe as mp
import json
import pickle


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


def trasnform_results(results:dict):
    '''
    Function to trasnform results with distance between points
    Args:
    results (dict): dictionary of results
    returns:
    points_transform (dict): dictionary of distances
    '''
    data = list(results.values())

    # Orden de distancias
    uni_pulgar = [0,1,2,3,4]
    uni_inidce = [0,5,6,7,8]
    uni_menique = [0,17,18,19,20]
    uni_corazon = [9,10,11,12]
    uni_anular = [13,14,15,16]
    uni_nudillos = [5,9,13,17]
    direcciones = [uni_pulgar,uni_inidce,uni_menique,uni_corazon,uni_anular,uni_nudillos]

    # Nuevos labels
    lbs = ['WT0','WT1','WT2','WT3','WI0','WI1','WI2','WI3','WP0','WP1','WP2','WP3','M0','M1','M2','R0','R1','R2','TI1','IM1','MP1']
    i = 0
    points_transform = {}
    for uni in direcciones:
       index_i = uni[0]
       for index in uni[1:]:
          points_transform[lbs[i]] = np.linalg.norm(np.array(data[index])-np.array(data[index_i]))
          i += 1
          index_i = index
    return points_transform


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
    
    return dic_results, True

    
def hands_detect(image:np.ndarray,plot:bool, on_predictions:bool=False):
    '''
    Detect hands in image
    ----------------------------------------------------------------
    Args:
    image (np.ndarray): image to detect hands in
    plot (bool): if True, plot the image
    on_predictions (bool): if False save predictions, but if true pass to model prediction

    Returns:
    flag (bool): if True, detect hands in image
    image_dr : image with points in hand
    dic_results: dictionary with information of hand detection
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
    flag = False
    dic_result = None

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

        if flag:    
            # Transform results
            dic_distances = trasnform_results(results=dic_result)
            if on_predictions:
               image_dw = model_predict(dic_distances,dic_result,image)
               return None, image_dw, None
            else: 
                # Save results
                with open('modules/static/temp/mp_results.json', 'w') as f:
                    json.dump(dic_result, f, indent=2)
                with open('modules/static/temp/mp_distances.json', 'w') as f:
                    json.dump(dic_distances, f, indent=2)
        

        # Draw hands
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                    image_dw, hand_landmarks, mp_hands.HAND_CONNECTIONS,mp_drawing.DrawingSpec(color=(255,255,0)))
        # Save drawings mp
        cv.imwrite('modules/static/temp/image_mp.jpg', image_dw)
        if plot:
            plot_image(image_dw, name_window='Result MediaPipe')
        
    # print(lb)
    return flag, image_dw, dic_result

def model_predict(distances:dict, result:dict, image:np.ndarray):
   '''
   Function to apply model prediction in distances array and plot the results
   Args:
   distances: dictionary for distances array
   result: dictionary for points array
   image: np.ndarray to plot
   Returns:
   image: np.ndarray with predictons
   '''

   # Cargar modelo
   model = pickle.load(open('modules/models/modelo_entrenado_RF.pickle', "rb"))
   map_model = {'A': 0, 'B': 1,'C': 2,'D': 3,'E': 4,'F': 5,'G': 6,
                           'H': 7,'I': 8,'J': 9,'K': 10,'L': 11,'M': 12,'N': 13,'Ñ': 14,
                           'O': 15,'P': 16,'Q': 17,'R': 18,'S': 19,'T': 20,'U': 21,'V': 22,
                           'W': 23,'X': 24,'Y': 25,'Z': 26}
   
    # Predicción
   distances = [list(distances.values())]
   try:
        index = model.predict(distances)
        letter = list(map_model.keys())[index[0]]
   except Exception as e:
       letter = ''
    
   # Draw result in image
   image =cv.flip(image, 1)
   h, w, _ = image.shape
   index_dw = [0,17,13,9,5]
   for cont,i in enumerate(index_dw):
        x = int(list(result.values())[i][0] * w)
        y = int(list(result.values())[i][1] * h)
        cv.circle(image, (x, y), 3,(255,255,0), 3)
        if cont == 0: 
            star = [x,y] ; star_0 = [x,y]
            cv.putText(image, letter, [star_0[0] + 10, star_0[1]+20], cv.FONT_HERSHEY_SIMPLEX, 2,(0,0,0), 4)

        elif i == index_dw[-1]:
            end = [x,y]
            cv.line(image, end, star, (0, 0, 255), 4)
            cv.line(image, end, star_0, (0, 0, 255), 4)
        else:
            end = [x,y]
            cv.line(image, star, end, (0, 0, 255), 4)
            star = end
    
   # plot_image(image=image, name_window='predict')
   return image
    


      

      
    
   
   
    


