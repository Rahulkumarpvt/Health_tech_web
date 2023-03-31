from flask import Flask, render_template, Response
from flask import request
import cv2
import datetime
import os
import base64
from flask import jsonify
from datetime import time
from time import *
from camera import capture

app = Flask(__name__)

camera = cv2.VideoCapture(0)

@app.route('/')
def index():
    """Home page"""
    return render_template('in.html')

@app.route('/save_image', methods=['POST'])
def save_image():
    """Route to save captured image"""
    image_data = request.get_json()['image_data']
    image_binary = base64.b64decode(image_data.split(',')[1])
    filename = os.path.join(app.static_folder, 'captures', f'image_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.png')
    with open(filename, 'wb') as f:
        f.write(image_binary)
    return jsonify({'status': 'success'})


def gen_frames(capture):
    """Generator function to generate video frames"""
    while True:
        frame = capture.get_frame()
        yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Route to generate video stream"""
    return Response(gen_frames(capture()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
    




# from flask import Flask, render_template, Response

# app = Flask(__name__)
# @app.route('/')
# def index():
#     return render_template("in.html")
# def gen_res():
# @app.route('/video_register')
# def video_register():
#     return Response(gen_res())

# if __name__ == '__main__':
#     app.run(host = '0.0.0.0', port = 5000, debug = True)