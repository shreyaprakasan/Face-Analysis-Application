from deepface import DeepFace as deepface
import os
import mysql.connector
import logging as log

log.basicConfig(
    filename='Logs.log', 
    level=log.INFO,
    format='%(asctime)s \n%(levelname)s :  %(message)s', 
    filemode="a"
)


def stream(h, u, p):
    
    try:
        cxn = mysql.connector.connect(
            host = h,
            user = u,
            password = p
        )

        try:
            current_dir = os.getcwd()
            temp_dir = os.path.join(current_dir, 'temporaryDir')
            os.mkdir(temp_dir)

            cursor = cxn.cursor()
            cursor.execute("USE faceanalysisapp;")
            cxn.commit()

            cursor.execute("SELECT * FROM analysis_dataset;")
            rows = cursor.fetchall()
            cursor.close()

            for row in rows:
                img_name = row[0]
                img_path = os.path.join(temp_dir, img_name)
                with open(img_path, 'wb') as file:
                    file.write(row[1])

            if os.path.exists(temp_dir):
                deepface.stream(temp_dir)

                # Removing temp directory after Face Analysis is complete
                for file in (os.listdir(temp_dir)):
                    p1 = os.path.join(temp_dir, file)
                    os.remove(p1)
                os.rmdir(temp_dir)
            else:
                log.error("[Face Analysis] Temporary Directory could not be created. Stream Failed.")

        except mysql.connector.Error as e:
                log.error(f"[Face Analysis | MySQL Connection] {e}")
                
    except mysql.connector.Error as e:
        log.error(f"[Face Analysis | MySQL Connection] {e}")

    

    



# attendance registration to mysql db
# do the same temp dir creation and deletion for Take_attendance