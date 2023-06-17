from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import QSize, Qt
import sys
import mysql.connector
import os
import logging as log

from Detection_Live_Video import detect
from Haar_Blink_Detection import detectBlink
from Emotion_Detection import detectEmotion
from Register_Face import registerface
from Face_Analysis import stream
from Register_Employee import registerEmployee
from Take_Attendance import takeAttendance

log.basicConfig(
    filename='Logs.log', 
    level=log.INFO,
    format='%(asctime)s \n%(levelname)s :  %(message)s', 
    filemode="a"
)

h = ''
u = ''
p = ''

bigButtonStyle1 = """
        QPushButton {
            background-color: rgba(83, 15, 166, 70); 
            color: rgb(28, 12, 82);
            letter-spacing: 0.5px;
            font-family: Tahoma;
            font-weight: 600;
            font-size: 20px;
            border: 2px solid rgb(7, 87, 18);
            border-radius: 5px;
        }
        QPushButton:hover {
            border: 2px solid white;
            background-color: rgb(7, 87, 18);
            color: white;
        }
"""

mainButtonStyle = """
                QPushButton {
                    background-color: rgba(157, 225, 252, 100); 
                    color: rgb(28, 12, 82);
                    letter-spacing: 0.5px;
                    font-family: Tahoma;
                    font-weight: 600;
                    font-size: 22px;
                    border: 2px solid white;
                    border-radius: 3px;
                }
                QPushButton:hover {
                    background-color: rgb(14, 57, 107);
                    color: white;
                }
            """

bigButtonStyle = """
                QPushButton {
                    background-color: rgba(83, 15, 166, 70); 
                    color: rgb(28, 12, 82);
                    letter-spacing: 0.5px;
                    font-family: Tahoma;
                    font-weight: 600;
                    font-size: 20px;
                    border: 2px solid white;
                    border-radius: 3px;
                }
                QPushButton:hover {
                    background-color: rgb(14, 57, 107);
                    color: white;
                }
            """

attendanceButtonStyle = """
                QPushButton {
                    background-color: rgba(135, 217, 250, 100); 
                    color: rgb(2, 11, 38);
                    letter-spacing: 0.6px;
                    font-family: Tahoma;
                    font-weight: 600;
                    font-size: 22px;
                    border: 2px solid white;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: rgb(14, 57, 107);
                    color: white;
                }
            """

backButtonStyle ='''
            QPushButton {
                border: 2px solid white;
                border-radius: 4px;
                font-style: italic;
                text-align: center;
                font-size: 17px;
                font-weight: 600;
                text-decoration: underline;
            }
            QPushButton:hover{
                background-color: rgba(255, 255, 255, 100);
            }
'''
textBoxStyle = '''
            QLineEdit {
                font-weight: 500;
                font-family: Courier;
                border-radius: 3px;
                font-size: 16px;
                
            }
'''

class WelcomeWindow(QMainWindow):
    def __init__(self):
    
        # Initializing Main Window
        super().__init__() 
        self.setWindowTitle('Face Detection & Analysis') 
        # self.setGeometry(300, 150, 780, 480)
        self.setFixedSize(880, 580)

        # Set Window background
        oImage = QImage('Icons_Images/window.png')
        sImage = oImage.scaled(QSize(880,580))                  
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))                        
        self.setPalette(palette)

        # Set App Icon
        appIcon = QIcon('Icons_Images/alien.png')
        self.setWindowIcon(appIcon)

        # Setting Central Widget
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        icon = QPixmap('Icons_Images/alien_2.png')
        iconLabel = QLabel(centralWidget)
        iconLabel.setPixmap(icon)
        iconLabel.resize(120, 120)
        iconLabel.move(380,20)

        heading = QLabel('<h1>Face Detection & Analysis</h1>',
                          centralWidget)
        heading.setStyleSheet("""
                QLabel {
                    font-family: Impact;
                    font-size: 34px;
                    letter-spacing: 2px;
               }
            """)
        
        #heading.setFont(QFont('Verdana', 11))
        heading.move(50,150)

        connect_info = QLabel('CONNECT TO MySQL TO GET STARTED', centralWidget)
        connect_info.setStyleSheet('''
                QLabel {
                    color: rgb(19, 7, 41);
                    font-family: Courier; 
                    font-weight: 700;
                    font-size: 26px;
                    letter-spacing: 1px;
                }
        ''')
        connect_info.move(180, 250)

        labels = ['MySQL HOST', 'MySQL USER', 'PASSWORD']
        box_labels = [QLabel(label) for label in labels]
        
        for label in box_labels:
            label.setStyleSheet('''
                    QLabel {
                        font-family: Tahoma;
                        color: black;
                        font-size: 18px;
                        font-weight: 600;
                    }
            ''')

        self.text_boxes = [QLineEdit() for _ in range(3)]
        for box in self.text_boxes:
            box.setStyleSheet(textBoxStyle)
            box.setFixedSize(200, 25)

        self.text_boxes[2].setEchoMode(QLineEdit.Password)
        # Adding labels, creating Registration Form.
        layout = QGridLayout()
        layout.addWidget(box_labels[0], 0, 0)
        layout.addWidget(self.text_boxes[0], 0, 1)

        layout.addWidget(box_labels[1], 1, 0)
        layout.addWidget(self.text_boxes[1], 1, 1)

        layout.addWidget(box_labels[2], 2, 0)
        layout.addWidget(self.text_boxes[2], 2, 1)

        layout.setSpacing(20)
        layout.setHorizontalSpacing(70)

        form = QFrame(centralWidget)
        form.setLayout(layout)
        form.move(240, 300)

        info = QLabel('ⓘ', centralWidget)
        info.setStyleSheet('''QLabel{font-size: 20px;}''')
        info.setToolTip('\'localhost\' for default local server')
        info.move(650, 315)

        button = QPushButton('CONNECT', centralWidget)
        button.setStyleSheet(bigButtonStyle1)
        button.setCursor(QCursor(Qt.PointingHandCursor))
        button.setFixedSize(200, 70)
        button.move(340,470)
        button.clicked.connect(self.connect)

        self.footer = QStatusBar()
        self.setStatusBar(self.footer)
        footerInfo = QLabel('<b> made by shreya ♥ </b>')
        self.footer.addWidget(footerInfo)
    
    def connect(self):
        global h 
        h = self.text_boxes[0].text()
        global u 
        u = self.text_boxes[1].text()
        global p 
        p = self.text_boxes[2].text()

        if not h or not u or not p:
            QMessageBox.information(self, "Warning", "Enter All Fields to Connect!")
        else:
            try:
                cxn = mysql.connector.connect (
                    host = h,
                    user = u,
                    password = p
                )
                cursor = cxn.cursor()
                log.info(f"[MySQL Connection] Connection Success with {u}@{h}")
                QMessageBox.information(self, "Success :)", "Connected to MySQL Server ! ")
                
                cursor.execute(f"SELECT SCHEMA_NAME FROM information_schema.SCHEMATA WHERE SCHEMA_NAME = 'FaceAnalysisApp'")
                result = cursor.fetchone()
                cursor.close()

                if not result:
                    cursor = cxn.cursor()
                    cursor.execute(f"CREATE DATABASE FaceAnalysisApp;")
                    cxn.commit()
                    cursor.close()
                    log.info("[MySQL Database] Database Created Successfully.")

                    cursor = cxn.cursor()
                    cursor.execute("USE FaceAnalysisApp;")
                    cxn.commit()
                    cursor.close()
                    log.info("[MySQL Database] Switched to Database Successfully.")

                    cursor = cxn.cursor()
                    cursor.execute("CREATE TABLE Employee_List(empID INT PRIMARY KEY, fName VARCHAR(50), lName VARCHAR(50), faceData MEDIUMBLOB);")
                    cxn.commit()
                    cursor.close()

                    cursor = cxn.cursor()
                    cursor.execute("CREATE TABLE Employee_Attendance(empID INT, date DATE, PRIMARY KEY (empID, date), FOREIGN KEY (empID) REFERENCES Employee_List (empID));")
                    cxn.commit()
                    cursor.close()

                    cursor = cxn.cursor()
                    cursor.execute("CREATE TABLE Analysis_Dataset (imgName VARCHAR(20), img MEDIUMBLOB);")
                    cxn.commit()
                    log.info("[MySQL Tables] Tables Created Successfully.")
                    cursor.close()

                else:
                    cursor = cxn.cursor()
                    cursor.execute("USE FaceAnalysisApp;")
                    cxn.commit()
                    log.info("[MySQL Database] Switched to Database Successfully.")
                    cursor.close()
                    
                self.open_main_window()

            except mysql.connector.Error as e:
                QMessageBox.information(self, "MySQL Connection Error ", "Re-Check Credentials. ")
                log.error(f'[MySQL Connection] {e}')

    def open_main_window(self):
        self.new_window = MainWindow()
        self.new_window.show()
        self.close()

class MainWindow(QMainWindow):
    def __init__(self):
    
        # Initializing Main Window
        super().__init__() 
        self.setWindowTitle('Face Detection & Analysis') 
        # self.setGeometry(300, 150, 780, 480)
        self.setFixedSize(880, 580)

        # Set Window background
        oImage = QImage('Icons_Images/window.png')
        sImage = oImage.scaled(QSize(880,580))                  
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))                        
        self.setPalette(palette)

        # Set App Icon
        appIcon = QIcon('Icons_Images/alien.png')
        self.setWindowIcon(appIcon)

        # Setting Central Widget
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        # Heading, Sub-Heading and Icon - QLABEL
        subHeading = QLabel('''<h3 style="letter-spacing :2px;font-weight:700;">
                            AN EFFICIENT SYSTEM FOR</h3>''', 
                            centralWidget)  
        subHeading.move(100,30)
        subHeading.setFont(QFont('Monospace', 10, 4, False))

        icon = QPixmap('Icons_Images/alien_1.png')
        iconLabel = QLabel(centralWidget)
        iconLabel.setPixmap(icon)
        iconLabel.move(20,40)
        iconLabel.resize(90, 90)

        heading = QLabel('<h1>Face Detection & Analysis</h1>',
                          centralWidget)
        heading.setStyleSheet("""
                QLabel {
                    font-family: Impact;
                    font-size: 32px;
               }
            """)
        #heading.setFont(QFont('Verdana', 11))
        heading.move(100,50)
        
        # LEFT SideMenu - QFRAME
        sideMenu1 = QFrame(centralWidget)

        # Vertical Button Layout for SideMenu - VBOX LAYOUT
        layout1 = QVBoxLayout()
        sideMenu1.setLayout(layout1)
        buttonTitles1 = ['DETECT FACE','DETECT EMOTIONS']
        for title in buttonTitles1:
            b = QPushButton(title)
            b.setObjectName(title)
            
            b.setFixedWidth(280)
            b.setFixedHeight(90)
            b.setStyleSheet(mainButtonStyle)
            # button.setFont(buttonFont)
            b.setCursor(QCursor(Qt.PointingHandCursor))
            layout1.addWidget(b)
            layout1.setStretchFactor(b, 2)
            layout1.addSpacing(12)

        sideMenu1.move(110, 170)
        
        # RIGHT Side Menu- QFrame
        sideMenu2 = QFrame(centralWidget)
        # Vertical Button Layout for RIGHT SideMenu - VBOX LAYOUT
        layout2 = QVBoxLayout()

        sideMenu2.setLayout(layout2)
        buttonTitles2 = ['DETECT BLINKING','FACE ANALYSIS']

        # Initializing buttons and setting stylesheet 'Mainbutton'
        for title in buttonTitles2:
            b = QPushButton(title)
            b.setObjectName(title)
            b.setFixedWidth(280)
            b.setFixedHeight(90)
            b.setStyleSheet(mainButtonStyle)
            b.setCursor(QCursor(Qt.PointingHandCursor))
            layout2.addWidget(b)
            layout2.setStretchFactor(b, 2)
            layout2.addSpacing(12)

        sideMenu2.move(450, 170)

        b1 = QPushButton('TAKE ATTENDANCE', centralWidget)
        b1.setObjectName('TAKE ATTENDANCE')
        b1.setFixedWidth(280)
        b1.setFixedHeight(100)
        b1.setStyleSheet(attendanceButtonStyle)
        b1.setCursor(QCursor(Qt.PointingHandCursor))
        b1.move(280, 420)
        b1.clicked.connect(self.open_take_attendance)

        # Setting Button Functionalities 
        b2 = self.findChild(QPushButton, 'DETECT BLINKING')
        b2.clicked.connect(self.execute_detect_blinking)

        b3 = self.findChild(QPushButton, 'DETECT FACE')
        b3.clicked.connect(self.execute_detect_face)

        b4 = self.findChild(QPushButton, 'DETECT EMOTIONS')
        b4.clicked.connect(self.open_detect_emotions)

        b5 = self.findChild(QPushButton, 'FACE ANALYSIS')
        b5.clicked.connect(self.open_face_analysis)

        self.footer = QStatusBar()
        self.setStatusBar(self.footer)
        footerInfo = QLabel('<b> made by shreya ♥ </b>')
        footerInfo.move(100, footerInfo.y())
        self.footer.addWidget(footerInfo)
    
    def execute_detect_face(self):
        detect()    
    
    def execute_detect_blinking(self):
        detectBlink()

    def open_face_analysis(self):
        self.new_window = AnalysisWindow()
        self.new_window.show()
        self.close()

    def open_detect_emotions(self):
        # previous_x, previous_y = self.geometry().x(), self.geometry().y()
        self.new_window = EmotionWindow()
        # self.new_window.move(previous_x, previous_y)
        self.new_window.show()
        self.close()
    
    def open_take_attendance(self):
        self.new_window = AttendanceWindow()
        self.new_window.show()
        self.close()

class EmotionWindow(QMainWindow):
    def __init__(self):
        super().__init__() 
        self.setWindowTitle('Face Detection & Analysis') 
        # self.setGeometry(300, 300, 780, 480)
        self.setFixedSize(880, 580)

        # Set Window background
        oImage = QImage('Icons_Images/window.png')
        sImage = oImage.scaled(QSize(880,580))                  
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))                        
        self.setPalette(palette)

        # Set App Icon
        appIcon = QIcon('Icons_Images/alien.png')
        self.setWindowIcon(appIcon)

        # Setting Central Widget
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        # Heading, Sub-Heading and Icon - QLABEL
        subHeading = QLabel('''<h3 style="letter-spacing :2px;font-weight:700;">
                            AN EFFICIENT SYSTEM FOR</h3>''', 
                            centralWidget)  
        subHeading.move(100,30)
        subHeading.setFont(QFont('Monospace', 10, 4, False))

        icon = QPixmap('Icons_Images/alien_1.png')
        iconLabel = QLabel(centralWidget)
        iconLabel.setPixmap(icon)
        iconLabel.move(20,40)
        iconLabel.resize(90, 90)

        heading = QLabel('<h1>Face Detection & Analysis</h1>', centralWidget)
        heading.setStyleSheet("""
                QLabel {
                    font-family: Impact;
                    font-size: 32px;
               }
            """)
    
        heading.move(100,50)

        heading_2 = QLabel('<h2>〚 Emotion Detection 〛</h2>', centralWidget)

        heading_2.setStyleSheet("""
                QLabel {
                    font-family: Palatino;
                    color: rgb(19, 7, 41);
                    font-size: 20px;
                    
               }
            """)
        heading_2.move(40, 170)

        capture_info = QLabel('Click a photo and detect the Dominant Emotion !', centralWidget)
        capture_info.setStyleSheet('''
                QLabel {
                    color: rgb(19, 7, 41);
                    font-family: Courier; 
                    font-weight: 600;
                    font-size: 26px;
                    letter-spacing: 1px;
                }
        ''')
        capture_info.move(40, 230)

        capture_button = QPushButton('CAPTURE ＆ DETECT', centralWidget)
        capture_button.setFixedSize(250, 80)
        capture_button.setStyleSheet(bigButtonStyle)
        capture_button.move(150, 340)
        capture_button.setCursor(QCursor(Qt.PointingHandCursor))
        capture_button.clicked.connect(self.execute_detect_emotions)

        cam_rules = QLabel(centralWidget)
        pixmap = QPixmap('Icons_Images/webcam_rules-modified.png')  
        scaled_pixmap = pixmap.scaled(210, 200, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)
        cam_rules.setPixmap(scaled_pixmap)
        cam_rules.move(500, 290)

        back_button = QPushButton('Back to Homepage', centralWidget)
        back_button.setStyleSheet(backButtonStyle)
        #back_button.setAlignment(Qt.AlignCenter) 
        back_button.setGeometry(10, 490, 180, 60)
        back_button.setCursor(QCursor(Qt.PointingHandCursor))
        back_button.clicked.connect(self.open_main_window)

        
    def open_main_window(self):
        # previous_x, previous_y = self.geometry().x(), self.geometry().y()
        self.new_window = MainWindow()
        # self.new_window.move(previous_x, previous_y)
        self.new_window.show()
        self.close()

    def execute_detect_emotions(self):
        detectEmotion()

class RegistrationWindow(QMainWindow):
      
    def __init__(self):
        super().__init__() 
        self.setWindowTitle('Face Detection & Analysis') 
        self.setFixedSize(880, 580)

        # Set Window background
        oImage = QImage('Icons_Images/window.png')
        sImage = oImage.scaled(QSize(880,580))                  
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))                        
        self.setPalette(palette)

        # Set App Icon
        appIcon = QIcon('Icons_Images/alien.png')
        self.setWindowIcon(appIcon)

        # Setting Central Widget
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        # Heading, Sub-Heading and Icon - QLABEL
        subHeading = QLabel('''<h3 style="letter-spacing :2px;font-weight:700;">
                            AN EFFICIENT SYSTEM FOR</h3>''', 
                            centralWidget)  
        subHeading.move(100,30)
        subHeading.setFont(QFont('Monospace', 10, 4, False))

        icon = QPixmap('Icons_Images/alien_1.png')
        iconLabel = QLabel(centralWidget)
        iconLabel.setPixmap(icon)
        iconLabel.move(20,40)
        iconLabel.resize(90, 90)

        heading = QLabel('<h1>Face Detection & Analysis</h1>', centralWidget)
        heading.setStyleSheet("""
                QLabel {
                    font-family: Impact;
                    font-size: 32px;
               }
            """)
    
        heading.move(100,50)

        heading_2 = QLabel('<h2>〚 Face Attendance 〛Employee Registration</h2>', centralWidget)

        heading_2.setStyleSheet("""
                QLabel {
                    font-family: Palatino;
                    color: rgb(19, 7, 41);
                    font-size: 20px;
                    
               }
            """)
        heading_2.move(40, 170)

        labels = ['Employee ID', 'First Name', 'Last Name']
        box_labels = [QLabel(label) for label in labels]
        
        for label in box_labels:
            label.setStyleSheet('''
                    QLabel {
                        font-family: Nirmala UI;
                        color: black;
                        font-size: 20px;
                        font-weight: 600;
                    }
            ''')

        self.text_boxes = [QLineEdit() for _ in range(3)]
        for box in self.text_boxes:
            box.setStyleSheet(textBoxStyle)
            box.setFixedSize(200, 23)

        # Adding labels, creating Registration Form.
        layout = QGridLayout()
        layout.addWidget(box_labels[0], 0, 0)
        layout.addWidget(self.text_boxes[0], 0, 1)

        self.text_boxes[0].setValidator(QIntValidator())

        layout.addWidget(box_labels[1], 1, 0)
        layout.addWidget(self.text_boxes[1], 1, 1)

        layout.addWidget(box_labels[2], 2, 0)
        layout.addWidget(self.text_boxes[2], 2, 1)

        layout.setSpacing(20)
        layout.setHorizontalSpacing(70)

        info = QLabel('ⓘ', centralWidget)
        info.setStyleSheet('''QLabel{font-size: 20px;}''')
        info.setToolTip('Only Number Input Allowed')
        info.move(640, 255)

        # Form of QFrame class with Grid Layout applied.
        form = QFrame(centralWidget)
        form.setLayout(layout)
        form.move(230, 240)

        button = QPushButton('REGISTER FACE', centralWidget)
        button.setStyleSheet(bigButtonStyle)
        button.setCursor(QCursor(Qt.PointingHandCursor))
        button.setFixedSize(200, 70)
        button.move(350,420)
        button.clicked.connect(self.register_employee)

        back_button = QPushButton('Back to Attendance', centralWidget)
        back_button.setStyleSheet(backButtonStyle)
        back_button.setGeometry(10, 490, 180, 60)
        back_button.setCursor(QCursor(Qt.PointingHandCursor))
        back_button.clicked.connect(self.open_attendance)

    def register_employee(self):
        input_id = self.text_boxes[0].text()
        input_fN = self.text_boxes[1].text()
        input_lN = self.text_boxes[2].text()

        if not input_id or not input_fN or not input_lN:
            QMessageBox.information(self, "EMPTY FIELDS ", "All Fields must be entered to Register !")
        else:
            registerEmployee()
            img_name = 'temp_employee.png'
            img_path = os.path.join(os.getcwd(), img_name)

            if os.path.exists(img_path):
                with open(img_path, 'rb') as file:
                    image_data = file.read()
                os.remove(img_path)

                try :
                    cxn = mysql.connector.connect(
                        host = h,
                        user = u,
                        password = p
                    )
                    try:
                        cursor = cxn.cursor()

                        query = "USE faceanalysisapp;"
                        cursor.execute(query)
                        cxn.commit()

                        query = "INSERT INTO employee_list VALUES (%s, %s, %s, %s)"
                        values = (input_id, input_fN, input_lN, image_data)
                        cursor.execute(query, values)
                        cxn.commit()
                        cursor.close()

                        log.info(f"[Register Employee | MySQL Insertion] Employee ID[{input_id}] Details Successfully Registered.")
                        QMessageBox.information(self, "Success !", "Employee has been registered successfully ☺")
                        self.open_attendance()

                    except mysql.connector.Error as e:
                        log.error(f"[Register Employee | MySQL Insertion] {e}")
                        QMessageBox.information(self, "Error !", "Invalid Entry")

                except mysql.connector.Error as e:
                    log.error(f"[Register Employee | MySQL Connection] {e}")
            
    def open_main_window(self):
        # previous_x, previous_y = self.geometry().x(), self.geometry().y()
        self.new_window = MainWindow()
        # self.new_window.move(previous_x, previous_y)
        self.new_window.show()
        self.close()

    def open_attendance(self):
        self.new_window = AttendanceWindow()
        self.new_window.show()
        self.close()

class AttendanceWindow(QMainWindow):
    def __init__(self):
        super().__init__() 
        self.setWindowTitle('Face Detection & Analysis') 
        # self.setGeometry(300, 300, 780, 480)
        self.setFixedSize(880, 580)

        # Set Window background
        oImage = QImage('Icons_Images/window.png')
        sImage = oImage.scaled(QSize(880,580))                  
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))                        
        self.setPalette(palette)

        # Set App Icon
        appIcon = QIcon('Icons_Images/alien.png')
        self.setWindowIcon(appIcon)

        # Setting Central Widget
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        # Heading, Sub-Heading and Icon - QLABEL
        subHeading = QLabel('''<h3 style="letter-spacing :2px;font-weight:700;">
                            AN EFFICIENT SYSTEM FOR</h3>''', 
                            centralWidget)  
        subHeading.move(100,30)
        subHeading.setFont(QFont('Monospace', 10, 4, False))

        icon = QPixmap('Icons_Images/alien_1.png')
        iconLabel = QLabel(centralWidget)
        iconLabel.setPixmap(icon)
        iconLabel.move(20,40)
        iconLabel.resize(90, 90)

        heading = QLabel('<h1>Face Detection & Analysis</h1>', centralWidget)
        heading.setStyleSheet("""
                QLabel {
                    font-family: Impact;
                    font-size: 32px;
               }
            """)
    
        heading.move(100,50)

        heading_2 = QLabel('<h2>〚 Face Recognition Attendance System 〛</h2>', centralWidget)

        heading_2.setStyleSheet("""
                QLabel {
                    font-family: Palatino;
                    color: rgb(19, 7, 41);
                    font-size: 20px;
                    
               }
            """)
        heading_2.move(40, 170)

        
        register_info = QLabel('New Employee ? ', centralWidget)
        register_info.setStyleSheet('''
                QLabel {
                    color: rgb(19, 7, 41);
                    font-family: Courier; 
                    font-weight: 700;
                    font-size: 25px;
                    letter-spacing: 1px;
                }
        ''')
        register_info.move(110, 280)

        register_button = QPushButton('REGISTER FACE', centralWidget)
        register_button.setFixedSize(250, 80)
        register_button.setStyleSheet(bigButtonStyle)
        register_button.move(120, 340)
        register_button.clicked.connect(self.open_registration)
        register_button.setCursor(QCursor(Qt.PointingHandCursor))

        take_attendance_info = QLabel('Already Registered ? ', centralWidget)
        take_attendance_info.setStyleSheet('''
                QLabel {
                    color: rgb(19, 7, 41);
                    font-family: Courier; 
                    font-weight: 700;
                    font-size: 25px;
                    letter-spacing: 1px;
                }
        ''')
        take_attendance_info.move(480, 280)

        attendance_button = QPushButton('TAKE ATTENDANCE', centralWidget)
        attendance_button.setFixedSize(250, 80)
        attendance_button.setStyleSheet(bigButtonStyle)
        attendance_button.move(500, 340)
        attendance_button.clicked.connect(self.execute_take_attendance)
        attendance_button.setCursor(QCursor(Qt.PointingHandCursor))


        back_button = QPushButton('Back to Homepage', centralWidget)
        back_button.setStyleSheet(backButtonStyle)
        back_button.setGeometry(10, 490, 180, 60)
        back_button.setCursor(QCursor(Qt.PointingHandCursor))
        back_button.clicked.connect(self.open_main_window)

    def open_main_window(self):
        self.new_window = MainWindow()
        self.new_window.show()
        self.close()
    
    def open_registration(self):
        self.new_window = RegistrationWindow()
        self.new_window.show()
        self.close()

    def execute_take_attendance(self):
        self.make_attendance_dir()
        takeAttendance(h, u, p)

    def make_attendance_dir(self):
        dir_path = os.path.join(os.getcwd(), 'temporaryDir')
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

        try:
            cxn = mysql.connector.connect(
                host = h,
                user = u,
                password = p
            )
            cursor = cxn.cursor()
            query = 'USE faceanalysisapp;'
            cursor.execute(query)
            cxn.commit()

            try:
                query = 'SELECT empID, fName, faceData from employee_list;'
                cursor.execute(query)
                rows = cursor.fetchall()
                cursor.close()

                for row in rows:
                    file_name = '{}_{}.png'.format(row[0], row[1])
                    file_path = os.path.join(dir_path, file_name)

                    with open(file_path, 'wb') as file:
                        file.write(row[2])
                log.info("[Take Attendance | Directory Created Successfully]")

            except mysql.connector.Error as e:
                log.error(f"[Take Attendance | MySQL Retrieve Information] {e}")

        except mysql.connector.Error as e:
            log.error(f"[Take Attendance | MySQL Connection] {e}")

class AnalysisWindow(QMainWindow):
    def __init__(self):
        super().__init__() 
        self.setWindowTitle('Face Detection & Analysis') 
        # self.setGeometry(300, 300, 780, 480)
        self.setFixedSize(880, 580)

        # Set Window background
        oImage = QImage('Icons_Images/window.png')
        sImage = oImage.scaled(QSize(880,580))                  
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))                        
        self.setPalette(palette)

        # Set App Icon
        appIcon = QIcon('Icons_Images/alien.png')
        self.setWindowIcon(appIcon)

        # Setting Central Widget
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        # Heading, Sub-Heading and Icon - QLABEL
        subHeading = QLabel('''<h3 style="letter-spacing :2px;font-weight:700;">
                            AN EFFICIENT SYSTEM FOR</h3>''', 
                            centralWidget)  
        subHeading.move(100,30)
        subHeading.setFont(QFont('Monospace', 10, 4, False))

        icon = QPixmap('Icons_Images/alien_1.png')
        iconLabel = QLabel(centralWidget)
        iconLabel.setPixmap(icon)
        iconLabel.move(20,40)
        iconLabel.resize(90, 90)

        heading = QLabel('<h1>Face Detection & Analysis</h1>', centralWidget)
        heading.setStyleSheet("""
                QLabel {
                    font-family: Impact;
                    font-size: 32px;
               }
            """)
    
        heading.move(100,50)

        heading_2 = QLabel('<h2>〚 Face Analysis 〛</h2>', centralWidget)

        heading_2.setStyleSheet("""
                QLabel {
                    font-family: Palatino;
                    color: rgb(19, 7, 41);
                    font-size: 20px;
                    
               }
            """)
        heading_2.move(40, 170)

        analysis_info = QLabel('Real-Time Face Recognition & Attribute Analysis!', centralWidget)
        analysis_info.setStyleSheet('''
                QLabel {
                    color: rgb(19, 7, 41);
                    font-family: Courier; 
                    font-weight: 600;
                    font-size: 26px;
                    letter-spacing: 1px;
                }
        ''')
        analysis_info.move(40, 230)
    
        info_icon = QPixmap('info.png')
        iconLabel = QLabel(centralWidget)
        iconLabel.setPixmap(info_icon)
        iconLabel.move(40,255)
        iconLabel.resize(90, 90)

        analysis_info2 = QLabel('Face must be Registered for Face Recognition during Analysis..', centralWidget)
        analysis_info2.setStyleSheet('''
                QLabel {
                    color: rgb(19, 7, 41);
                    font-family: Yu Gothic UI Semibold;
                    font-weight: 600;
                    font-size: 20px;
                    letter-spacing: 1px;
                }
        ''')
        analysis_info2.move(90, 285)

        register_button = QPushButton('REGISTER', centralWidget)
        register_button.setFixedSize(250, 80)
        register_button.setStyleSheet(bigButtonStyle)
        register_button.move(140, 360)
        register_button.setCursor(QCursor(Qt.PointingHandCursor))
        register_button.clicked.connect(self.execute_register_face)

        attendance_button = QPushButton('ANALYZE', centralWidget)
        attendance_button.setFixedSize(250, 80)
        attendance_button.setStyleSheet(bigButtonStyle)
        attendance_button.move(480, 360)
        attendance_button.setCursor(QCursor(Qt.PointingHandCursor))
        attendance_button.clicked.connect(self.execute_face_analysis)

        back_button = QPushButton('Back to Homepage', centralWidget)
        back_button.setStyleSheet(backButtonStyle)
        back_button.setGeometry(10, 490, 180, 60)
        back_button.setCursor(QCursor(Qt.PointingHandCursor))
        back_button.clicked.connect(self.open_main_window)
    
    def open_main_window(self):
        self.new_window = MainWindow()
        self.new_window.show()
        self.close()
    
    def execute_register_face(self):
        registerface()
        current_dir = os.getcwd()
        temp_path = os.path.join(current_dir, 'temp_face.png')

        if os.path.exists(temp_path):
            with open(temp_path, 'rb') as file:
                image_data = file.read()
            os.remove(temp_path)
            # print(h +" "+u+ " "+p)
            cxn = mysql.connector.connect(
                host = h,
                user = u,
                password = p
            )
            cursor = cxn.cursor()
            cursor.execute("USE faceanalysisapp;")
            cxn.commit()
            cursor.close()

            cursor = cxn.cursor()
            cursor.execute("SELECT count(*) FROM analysis_dataset;")
            count = cursor.fetchone()
            res = count[0] + 1
            cursor.close()
            file_name = "captured_{}.png".format(str(res).zfill(5))

            cursor = cxn.cursor()
            sql = "INSERT INTO analysis_dataset VALUES (%s, %s)"
            values = (file_name, image_data)
            cursor.execute(sql, values)

            cxn.commit()
            cursor.close()

    def execute_face_analysis(self):
        QMessageBox.information(self, 'Starting Stream ...', 'Press \'q\' to EXIT Stream.')
        stream(h, u, p)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WelcomeWindow()
    window.show()
    sys.exit(app.exec_())

