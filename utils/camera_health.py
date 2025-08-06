import cv2

def check_camera(index=0):
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        return False
    ret, _ = cap.read()
    cap.release()
    return ret
