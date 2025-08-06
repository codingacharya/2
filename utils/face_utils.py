from deepface import DeepFace
import numpy as np
import os

def identify_employee(frame):
    try:
        result = DeepFace.find(img_path=frame, db_path="employee_db", model_name="Facenet", enforce_detection=False)
        if len(result[0]) > 0:
            identity_path = result[0]['identity'][0]
            emp_id = os.path.basename(identity_path).split('.')[0]
            score = result[0]['Facenet_cosine'][0]
            return emp_id, score
        else:
            return None, 0.0
    except Exception as e:
        print("Face Recognition Error:", e)
        return None, 0.0
