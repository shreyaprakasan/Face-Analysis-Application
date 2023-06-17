import cv2 as cv
import numpy as np
import os
from datetime import datetime as dt

# Callback function for mouse events
def clicked_exit(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        # Check if the click is within the button region
        if x >= button_x and x <= button_x + b_width and y >= button_y and y <= button_y + b_height:
            cam = param
            cam.release()
            cv.destroyAllWindows()
            

# Face and eye cascade classifiers from xml files
xml_path1 = os.path.join(os.path.dirname(__file__), 'haarcascade_frontalface_alt.xml')
xml_path2 = os.path.join(os.path.dirname(__file__), 'haarcascade_eye_tree_eyeglasses.xml')

face_cascade = cv.CascadeClassifier(xml_path1)
eye_cascade = cv.CascadeClassifier(xml_path2)


current = dt.now().strftime("%H:%M%p")
window_name = 'Eye Blink Detection | Started [{}]'.format(current)

pad_x, pad_y = 100, 100

# Exit Button properties
b_width = 150
b_height = 50
b_color = (95, 5, 250)  
button_x = 10
button_y = 500

# Starting the video capture

def detectBlink():
    cam = cv.VideoCapture(0)
    blink_counter = -1
    is_blinking = False

    while True:
        ret, frame = cam.read()
        frame = cv.flip(frame, 1)

        if not ret:
            cv.destroyAllWindows()
            break

        frame_height, frame_width = frame.shape[0] - 100, frame.shape[1] - 100
        window_width = frame_width + 2*pad_x 
        window_height = frame_height + 2*pad_y 

        background = np.zeros((window_height, window_width, 3), dtype=np.uint8)

        frame = cv.resize(frame, (frame_width, frame_height))

        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        # Applying filter to remove impurities
        gray = cv.bilateralFilter(gray, 5, 1, 1)

        
        faces = face_cascade.detectMultiScale(gray, 1.3, 5, minSize=(200, 200))
        if len(faces) > 0:
            for (x, y, w, h) in faces:
                cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Extract the region of interest (ROI) which contains the face
                roi_face = gray[y:y + h, x:x + w]
                
                # Detect eyes within the ROI 
                eyes = eye_cascade.detectMultiScale(roi_face, 1.3, 5, minSize=(50, 50)) # 1.3 - reduction scale size factor, 5 - min. neighbours, (50, 50) - min. detection size

                # if len(eyes) != 0:
                if  len(eyes)>= 2:
                    # If not blinking, set is_blinking to True and increment blink counter
                    if not is_blinking:
                        blink_counter += 1
                        is_blinking = True

                    cv.putText(background, "Eyes Detected! Blinks: {}".format(blink_counter), (100, 80), cv.FONT_HERSHEY_SIMPLEX, 0.9, (229, 64, 247), 2)
                elif len(eyes) == 0 and is_blinking:
                    is_blinking = False

        else:
            cv.putText(frame, "[No face(s) detected]", (65, 140), cv.FONT_HERSHEY_PLAIN, 2.2, (3, 32, 252), 2)

        # Drawing EXIT button border [ -1 thickness to FILL rectangle, not outline rectangle ]
        cv.rectangle(background, (button_x, button_y), (button_x + b_width, button_y + b_height), b_color, -1)
        cv.putText(background, "CLOSE", (button_x + 10, button_y + 30), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # Naming window to use to call 'exit_clicked()'
        cv.namedWindow(window_name)
        # Set the mouse callback function
        cv.setMouseCallback(window_name, clicked_exit, cam)

        # Display the embedded frame in background window
        background[pad_y:pad_y + frame_height, pad_x:pad_x + frame_width] = frame
        cv.imshow(window_name, background)

        # Window ERROR without waitKey()
        cv.waitKey(1)
