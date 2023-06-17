import cv2 as cv
from deepface import DeepFace as deepface
from datetime import datetime, date
import numpy as np
import os
import mysql.connector
import logging as log

log.basicConfig(
    filename='Logs.log', 
    level=log.INFO,
    format='%(asctime)s \n%(levelname)s :  %(message)s', 
    filemode="a"
)

def clicked_exit(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        # Check if the click is within the button region
        if x >= button_x and x <= button_x + b_width and y >= button_y and y <= button_y + b_height:
            cam = param
            cv.destroyAllWindows()
            cam.release()

current_dt = datetime.now().strftime("%H:%M%p")
window_name = 'Take Attendance | Started [{}]'.format(current_dt)
# Padding around video stream
pad_x, pad_y = 100, 100

# Exit Button properties
b_width = 150
b_height = 50
b_color = (95, 5, 250)  
button_x = 10
button_y = 500


temp_path = os.path.join(os.getcwd(), 'temp_employee.png')
dir_path = os.path.join(os.getcwd(), 'temporaryDir')

# Exited variable required in case user CLOSES camera window before capturing.
def takeAttendance(h, u, p):
    cam = cv.VideoCapture(0)

    identified = False
    exited = False
    marked = False

    while True:
        ret, frame = cam.read()
        if not ret:
            cv.destroyAllWindows()
            exited = True
            break

        frame = cv.flip(frame, 1)
        # Set the desired window and frame size
        frame_height, frame_width = frame.shape[0] - 100, frame.shape[1] - 100
        frame = cv.resize(frame, (frame_width, frame_height))
        window_width = frame_width + 2*pad_x 
        window_height = frame_height + 2*pad_y 
        
        x = window_width - (frame_width + pad_x) - 10
        y = window_height - (frame_height + pad_y) - 20

        background = np.zeros((window_height, window_width, 3), dtype=np.uint8)
      
        background[pad_y:pad_y + frame_height, pad_x:pad_x + frame_width] = frame
        text = 'When you\'re ready, Press ENTER to Capture'
        
        # Instruction Text
        cv.putText(background, text, (x, y), cv.FONT_HERSHEY_SIMPLEX, 0.9, (182, 149, 252), 2)

        # Drawing CLOSE button border [ -1 thickness to FILL rectangle, not outline rectangle ]
        cv.rectangle(background, (button_x, button_y), (button_x + b_width, button_y + b_height), b_color, -1)
        cv.putText(background, "CLOSE", (button_x + 10, button_y + 30), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv.namedWindow(window_name)
        # Set the mouse callback function
        cv.setMouseCallback(window_name, clicked_exit, cam)
        cv.imshow(window_name, background)

        if cv.waitKey(1) == 13:
            cv.imwrite(temp_path, frame)
            cv.destroyAllWindows()
            img = cv.imread(temp_path)
            break

    if not exited:
        res = deepface.find(img_path=temp_path, db_path=dir_path, enforce_detection=False)[0]
        if len(res) > 0:
            identified = True
            match = res.iloc[0]
            recog_file = match['identity'][:-4]
            recog_name = recog_file.split('/')[1]
            recog_split = recog_name.split('_')

            # x, y, w, h = res['source_x'], res['source_y'], res['source_w'], res['source_h']

            window_name_2 = 'IMAGE CAPTURED - Attendance'
            background = np.zeros((window_height, window_width, 3), dtype=np.uint8)
            background[pad_y:pad_y + frame_height, pad_x:pad_x + frame_width] = img
            text = 'Employee Identified : ID [{}], Name [{}]'.format(recog_split[0], recog_split[1])
            # print(text)
            # Putting Face Identified text
            cv.putText(background, text, (x, y), cv.FONT_HERSHEY_PLAIN, 1.5, (252, 162, 203), 2)

            # EXIT button
            cv.rectangle(background, (button_x, button_y), (button_x + b_width, button_y + b_height), b_color, -1)
            cv.putText(background, "CLOSE", (button_x + 10, button_y + 30), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv.namedWindow(window_name_2)
            cv.setMouseCallback(window_name_2, clicked_exit, cam)

            cv.imshow(window_name_2, background)
            cv.waitKey(0)
        else:
            window_name_2 = 'IMAGE CAPTURED - Attendance'
            background = np.zeros((window_height, window_width, 3), dtype=np.uint8)
            background[pad_y:pad_y + frame_height, pad_x:pad_x + frame_width] = img

            text = 'Employee NOT Identified'
            # Putting Face Identified text
            cv.putText(background, text, (x, y), cv.FONT_HERSHEY_PLAIN, 2, (252, 162, 203), 2)

            # EXIT button
            cv.rectangle(background, (button_x, button_y), (button_x + b_width, button_y + b_height), b_color, -1)
            cv.putText(background, "CLOSE", (button_x + 10, button_y + 30), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv.namedWindow(window_name_2)
            cv.setMouseCallback(window_name_2, clicked_exit, cam)

            cv.imshow(window_name_2, background)
            cv.waitKey(0)

    if identified:
        # Get Current Date and Time to mark Attendance
        current_date = date.today()
        current_time = datetime.now().time()

        try:
            cxn = mysql.connector.connect(
                host = h,
                user = u,
                password = p
            )
            try:
                cursor = cxn.cursor()
                cursor.execute('USE faceanalysisapp;')
                cxn.commit()

                query = 'INSERT INTO employee_attendance VALUES (%s, %s, %s);'
                values = (recog_split[0], current_date, current_time)
                cursor.execute(query, values)
                cxn.commit()
                cursor.close()

                marked = True
                log.info(f'[Mark Attendance | MySQL Insertion] Employee {recog_split[0]} Attendance Marked Successfully.')

            except mysql.connector.Error as e:
                log.error(f"[Mark Attendance | MySQL Insertion] {e}")
                window_name_3 = 'ERROR | Attendance Not Marked'
                background = np.zeros((window_height, window_width, 3), dtype=np.uint8)
                background[pad_y:pad_y + frame_height, pad_x:pad_x + frame_width] = img
                text = 'Attendance already Marked.'
                cv.putText(background, text, (x, y), cv.FONT_HERSHEY_PLAIN, 2, (182, 149, 252), 2)

                # Timeout instead of CLOSE button
                cv.imshow(window_name_3, background)
                cv.waitKey(2000)
                cv.destroyAllWindows()

        except mysql.connector.Error as e:
            log.error(f"[Mark Attendance | MySQL Connection] {e}")

        if marked:
            window_name_4 = 'SUCCESS | Attendance Marked'
            background = np.zeros((window_height, window_width, 3), dtype=np.uint8)
            background[pad_y:pad_y + frame_height, pad_x:pad_x + frame_width] = img
            text = 'Attendance has been Marked Successfully !'
            cv.putText(background, text, (x, y), cv.FONT_HERSHEY_PLAIN, 2, (182, 149, 252), 2)

            # Timeout instead of CLOSE button
            cv.imshow(window_name_4, background)
            cv.waitKey(2000)
            cv.destroyAllWindows()

    if os.path.exists(temp_path):       
        os.remove(temp_path)

    for file in os.listdir(dir_path):
        os.remove(os.path.join(dir_path, file))

    os.rmdir(dir_path)
    

 