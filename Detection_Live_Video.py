import cv2 as cv
import os
from datetime import datetime as dt
import numpy as np

# Callback function for mouse events
def clicked_exit(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        # Check if the click is within the button region
        if x >= button_x and x <= button_x + b_width and y >= button_y and y <= button_y + b_height:
            cv.destroyAllWindows()
            cam = param
            cam.release()

# Exit Button properties
b_width = 150
b_height = 50
b_color = (95, 5, 250)  
button_x = 10
button_y = 500


# def detect():

xml_path = os.path.join(os.path.dirname(__file__), 'haarcascade_frontalface_alt.xml')
faceCascade = cv.CascadeClassifier(xml_path)

current_dt = dt.now().strftime("%H:%M%p")
window_name = 'Video Stream | Started [{}]'.format(current_dt)
# Padding around video stream
pad_x, pad_y = 100, 100


def detect():
    cam = cv.VideoCapture(0)

    # print('reached detect')
    while True:
        ret, frame = cam.read()
        frame = cv.flip(frame, 1)

        if not ret:
            cv.destroyAllWindows()
            # cam.release()
            break

        # Set the desired window and frame size
        frame_height, frame_width = frame.shape[0] - 100, frame.shape[1] - 100
        frame = cv.resize(frame, (frame_width, frame_height))
        window_width = frame_width + 2*pad_x 
        window_height = frame_height + 2*pad_y 
        
        background = np.zeros((window_height, window_width, 3), dtype=np.uint8)

        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
        )

        n_detected = len(faces)

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv.rectangle(
                frame, 
                (x, y), 
                (x+w, y+h), 
                (255, 166, 172), 
                3    
            )
        # background[50,50] = logo
        background[pad_y:pad_y + frame_height, pad_x:pad_x + frame_width] = frame
        text = '{} Face(s) Detected'.format(n_detected)
        
        # No. of faces detected - Text
        cv.putText(background, text, (100, 90), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Drawing EXIT button border [ -1 thickness to FILL rectangle, not outline rectangle ]
        cv.rectangle(background, (button_x, button_y), (button_x + b_width, button_y + b_height), b_color, -1)

        cv.putText(background, "CLOSE", (button_x + 10, button_y + 30), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv.namedWindow(window_name)
        # Set the mouse callback function
        cv.setMouseCallback(window_name, clicked_exit, cam)
        cv.imshow(window_name, background)
        cv.waitKey(1)

