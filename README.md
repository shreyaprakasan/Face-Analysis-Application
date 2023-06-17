# Face-Analysis-Application
### A Python application built to perform face detection, recognition and other analysis tasks. 

This application has the following functionalities:
  * Attendance Marking using Face Recognition
  * Face Detection
  * Eye Blink Detection
  * Emotion Detection
  * Face Analysis
  

A MySQL Database was used to store all registered faces and other attendance details, and the frontend is built using Python's PySide2 library. 

<br>
<img width="473" alt="Face Analysis App - Home Screen to enter user MySQL credentials" src="https://github.com/shreyaprakasan/Face-Analysis-Application/assets/87723447/97c4f83e-f6d6-45d0-9c14-55cf8a04344d"><br><br>

For a new user, the app automatically creates the required schemas and tables, once the MySQL-server user credentials are entered.

The user must have **a MySQL Server successfully started** in the background, in order to use the **Face Analysis (for face recognition only)** or **Attendance Marking** functionalities.

### Run the Home_UI.py file to start the application.

--------------------------------------------------------------------------------------------------------------------------------------------------

The main libraries used in this project are:
 * OpenCV
    * Webcam streaming
    * Face and Eye detection using HaarCascades (shipped with OpenCV)
 * DeepFace
    * Emotion Detection
    * Face Analysis (includes Gender, Age, Emotion analysis and Face Recognition)
    * Face Recognition
 * mysql-connector for MySQL Connections 
 * PySide2 for the Application UI 

