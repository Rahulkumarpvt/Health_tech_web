import face_recognition
import cv2
import numpy as np
import mysql.connector
import base64
from PIL import Image
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

cnx = mysql.connector.connect(
    user='root', password='dbpass', host='localhost', database='face_recognition')
cursor = cnx.cursor()


@app.route('/')
def home():
    return render_template('home.html')


def img_enc_dec(name_path):
    with open(name_path, 'rb') as f:
        image = f.read()
    with open(name_path, 'wb') as f:
        image = bytearray(image)
        for index, values in enumerate(image):
            image[index] = values ^ 12
        f.write(image)


@app.route('/login', methods=['GET', 'POST'])
def login():
    mesage = ''
    if request.method == 'POST':
        user = request.form['name']
        if len(user) < 1:
            mesage = 'Please Enter Username!!!'
        else:
            p_data = request.form['pic']
            p_data = p_data.replace("data:image/png;base64,", "")
            p_bytes = base64.b64decode(p_data)
            photo = cv2.imdecode(np.frombuffer(p_bytes, np.uint8), -1)
            Image.fromarray(photo).save("image\\{}".format("logimg.png"))
            cursor.execute(
                'select photo from users where username=%s', (user,))
            res = cursor.fetchone()
            if res:
                res = res[0]
                res = base64.b64decode(res).decode()

                try:
                    img_enc_dec("image\\{}".format(res))
                    known_image = face_recognition.load_image_file(
                        "image\\{}".format(res))
                    unknown_image = face_recognition.load_image_file(
                        "image\\logimg.png")
                    known_encode = face_recognition.face_encodings(known_image)[
                        0]
                    unknown_encode = face_recognition.face_encodings(unknown_image)[
                        0]
                    face_compare = face_recognition.compare_faces(
                        [known_encode], unknown_encode)
                    if res and face_compare[0]:
                        session['loggedin'] = True

                        mesage = "Logged In Successfully"
                        img_enc_dec("image\\logimg.png")
                        img_enc_dec("image\\{}".format(res))

                        return render_template('user.html', mesage=mesage)
                    else:
                        mesage = "Incorrect Credentials"
                except:
                    mesage = "Face could not recognisied!!!"
            else:
                mesage = "User Not Found!!"
    return render_template('login.html', mesage=mesage)


@app.route('/register', methods=['GET', 'POST'])
def register():
    mesage = ''
    if request.method == 'POST' and 'name' in request.form and 'pic' in request.form:
        user = request.form['name']
        if len(user) < 1:
            mesage = 'Please Enter Username!!!'
        else:
            p_data = request.form['pic']
            p_data = p_data.replace("data:image/png;base64,", "")
            p_bytes = base64.b64decode(p_data)
            try:
                photo = cv2.imdecode(np.frombuffer(p_bytes, np.uint8), -1)
                q = 'select * from users where username = %s'
                cursor.execute(q, (user,))
                res = cursor.fetchone()
                if res:
                    mesage = 'ALready Exist'
                else:
                    iname = user+'.png'
                    Image.fromarray(photo).save("image\\{}".format(iname))
                    known_image = face_recognition.load_image_file(
                        "image\\{}".format(iname))
                    known_encode = face_recognition.face_encodings(known_image)[
                        0]
                    img_enc_dec("image\\{}".format(iname))
                    iname = base64.b64encode(iname.encode())

                    cursor.execute(
                        'INSERT INTO users VALUES ( %s ,%s)', (user, iname))
                    cnx.commit()
                    mesage = "Registered Successful"

            except:
                mesage = "Please ensure that your face is well-lit and clearly visible to the camera!"
    elif request.method == 'POST':
        mesage = 'Please fill out the form !'
    return render_template('register.html', mesage=mesage)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.secret_key = 'secret'
    app.run(debug=True)
cursor.close()
cnx.close()
