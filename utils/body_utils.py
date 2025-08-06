import mediapipe as mp
import numpy as np

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True)

def extract_body_vector(frame):
    results = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    if not results.pose_landmarks:
        return None
    landmarks = results.pose_landmarks.landmark
    body_vector = np.array([[lm.x, lm.y, lm.z] for lm in landmarks]).flatten()
    return body_vector
