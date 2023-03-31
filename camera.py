import cv2
from PIL import Image


class capture():
    def __init__(self):
        self.cam = cv2.VideoCapture(0)
    def __del__(self):
        self.cam.release()
    def get_frame(self):
        success, frame = self.cam.read()
        ret, buffer = cv2.imencode('.jpg', frame)
        return buffer.tobytes()

