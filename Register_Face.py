import cv2 as cv
from datetime import datetime as dt
import numpy as np
import os

def clicked_exit(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        # Check if the click is within the button region
        if x >= button_x and x <= button_x + b_width and y >= button_y and y <= button_y + b_height:
            cam = param
            cam.release()
            cv.destroyAllWindows()

current_dt = dt.now().strftime("%H:%M%p")
window_name = 'Register Face | Started [{}]'.format(current_dt)
# Padding around video stream
pad_x, pad_y = 100, 100

# Exit Button properties
b_width = 150
b_height = 50
b_color = (95, 5, 250)  
button_x = 10
button_y = 500


current_dir = os.getcwd()
temp_path = os.path.join(current_dir, 'temp_face.png')


def registerface():
    cam = cv.VideoCapture(0)

    while True:
        ret, frame = cam.read()

        if not ret:
            cv.destroyAllWindows()
            break

        frame = cv.flip(frame, 1)
        # Set the desired window and frame size
        frame_height, frame_width = frame.shape[0] - 100, frame.shape[1] - 100
        frame = cv.resize(frame, (frame_width, frame_height))
        window_width = frame_width + 2*pad_x 
        window_height = frame_height + 2*pad_y 
        
        background = np.zeros((window_height, window_width, 3), dtype=np.uint8)
       
        background[pad_y:pad_y + frame_height, pad_x:pad_x + frame_width] = frame
        text = 'When you\'re ready, Press ENTER to Capture'
        
        # Instruction Text
        cv.putText(background, text, (60, 88), cv.FONT_HERSHEY_SIMPLEX, 0.9, (182, 149, 252), 2)

        # Drawing CLOSE button border [ -1 thickness to FILL rectangle, not outline rectangle ]
        cv.rectangle(background, (button_x, button_y), (button_x + b_width, button_y + b_height), b_color, -1)
        cv.putText(background, "CLOSE", (button_x + 10, button_y + 30), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv.namedWindow(window_name)
        # Set the mouse callback function
        cv.setMouseCallback(window_name, clicked_exit, cam)
        cv.imshow(window_name, background)

        if cv.waitKey(1) == 13:
            cv.destroyAllWindows()
            cv.imwrite(temp_path, frame)
            window_name1 = 'Image Captured [{}]'.format(current_dt)
            background = np.zeros((window_height, window_width, 3), dtype=np.uint8)
            background[pad_y:pad_y + frame_height, pad_x:pad_x + frame_width] = frame
            text = 'Image Captured Successfully !'
            
            # Info Text
            cv.putText(background, text, (60, 88), cv.FONT_HERSHEY_SIMPLEX, 0.9, (182, 149, 252), 2)
            cv.namedWindow(window_name)
            cv.imshow(window_name1, background)
            cv.waitKey(2000)
            cv.destroyAllWindows()
            break

