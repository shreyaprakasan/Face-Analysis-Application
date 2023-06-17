from deepface import DeepFace as deepface
import cv2 as cv
from datetime import datetime as dt
import numpy as np
import os

# Callback function for mouse events
def clicked_exit(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        # Check if the click is within the button region
        if x >= button_x and x <= button_x + b_width and y >= button_y and y <= button_y + b_height:
            cam = param
            cv.destroyAllWindows()
            cam.release()

current_dt = dt.now().strftime("%H:%M%p")
window_name = 'Emotion Detection | Started [{}]'.format(current_dt)
# Padding around video stream
pad_x, pad_y = 100, 100

# Exit Button properties
b_width = 150
b_height = 50
b_color = (95, 5, 250)  
button_x = 10
button_y = 500


current_dir = os.getcwd()
temp_path = os.path.join(current_dir, 'temp_employee.png')

def detectEmotion():
    cam = cv.VideoCapture(0)
    exited = False
    while True:
        ret, frame = cam.read()
        frame = cv.flip(frame, 1)

        if not ret:
            exited = True
            cv.destroyAllWindows()
            break

        # Set the desired window and frame size
        frame_height, frame_width = frame.shape[0] - 100, frame.shape[1] - 100
        frame = cv.resize(frame, (frame_width, frame_height))
        window_width = frame_width + 2*pad_x 
        window_height = frame_height + 2*pad_y 
        
        background = np.zeros((window_height, window_width, 3), dtype=np.uint8)

        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        
        background[pad_y:pad_y + frame_height, pad_x:pad_x + frame_width] = frame
        text = 'When you\'re ready, Press ENTER to Capture'
        
        x = window_width - (frame_width + pad_x) - 10
        y = window_height - (frame_height + pad_y) - 20
        # Instruction Text
        cv.putText(background, text, (x, y), cv.FONT_HERSHEY_SIMPLEX, 0.9, (182, 149, 252), 2)

        # Drawing EXIT button border [ -1 thickness to FILL rectangle, not outline rectangle ]
        cv.rectangle(background, (button_x, button_y), (button_x + b_width, button_y + b_height), b_color, -1)
        cv.putText(background, "CLOSE", (button_x + 10, button_y + 30), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv.namedWindow(window_name)
        cv.setMouseCallback(window_name, clicked_exit, cam)
        cv.imshow(window_name, background)

        if cv.waitKey(1) == 13:
            cv.putText(background, "IMAGE CAPTURED", (button_x + 40, button_y + 30), cv.FONT_HERSHEY_SIMPLEX, 1, (39, 237, 36), 2)
            cv.imwrite(temp_path, frame)
            cv.waitKey(2000)
            cv.destroyAllWindows()
            img = cv.imread(temp_path)
            break

    if not exited:
        try:
            obj = deepface.analyze(img_path = temp_path, actions = 'emotion')[0]
            emotion = obj['dominant_emotion']
            val = round(obj['emotion'][emotion], 1)
            text = "Dominant Emotion : {} [{}%]".format(emotion,val)
            x, y, w, h = obj['region'].values()

            # Drawing rectangle around the face detected
            cv.rectangle(
                    img,
                    (x, y),
                    (x + w, y + h),
                    (229, 64, 247),
                    2
                )
            window_name_2 = 'IMAGE CAPTURED - Detected Emotion'
            background = np.zeros((window_height, window_width, 3), dtype=np.uint8)
            background[pad_y:pad_y + frame_height, pad_x:pad_x + frame_width] = img

            # Putting Emotion detected text
            x = window_width - (frame_width + pad_x) - 10
            y = window_height - (frame_height + pad_y) - 20
            cv.putText(background, text, (x, y), cv.FONT_HERSHEY_PLAIN, 2, (182, 149, 252), 2)

            # EXIT button
            cv.rectangle(background, (button_x, button_y), (button_x + b_width, button_y + b_height), b_color, -1)
            cv.putText(background, "CLOSE", (button_x + 10, button_y + 30), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv.namedWindow(window_name_2)
            cv.setMouseCallback(window_name_2, clicked_exit, cam)
            cv.imshow(window_name_2, background)
            cv.waitKey(0)
        except ValueError:
            background = np.zeros((window_height, window_width, 3), dtype=np.uint8)
            background[pad_y:pad_y + frame_height, pad_x:pad_x + frame_width] = img
            text = 'NO FACES DETECTED'
            cv.putText(background, text, (160, 80), cv.FONT_HERSHEY_PLAIN, 2.5, (2, 2, 250), 2)
            window_name_2 = 'IMAGE CAPTURED - Detection ERROR'
            cv.rectangle(background, (button_x, button_y), (button_x + b_width, button_y + b_height), b_color, -1)
            cv.putText(background, "CLOSE", (button_x + 10, button_y + 30), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv.namedWindow(window_name_2)
            cv.setMouseCallback(window_name_2, clicked_exit, cam)
            cv.imshow(window_name_2, background)
            cv.waitKey(0)        
    if os.path.exists(temp_path):
        os.remove(temp_path)
