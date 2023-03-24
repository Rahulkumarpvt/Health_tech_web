import cv2
import numpy as np
import sys
import face_recognition
from PIL import Image


cascpath = "harcasface.xml"
def check():
    known_image = face_recognition.load_image_file("f3.jpg")
    unknown_image = face_recognition.load_image_file("f4.jpg")
    print(known_image)
    print(unknown_image)
    print(face_recognition.face_encodings(unknown_image))
    known_encode = face_recognition.face_encodings(known_image)[0]
    unknown_encode = face_recognition.face_encodings(unknown_image)[0]

    res = face_recognition.compare_faces([known_encode],unknown_encode)
    return res
def reg():
    faces = ()
# cascpath = "he.xml"
    fc = cv2.CascadeClassifier(cascpath)
    vc = cv2.VideoCapture(0)
    while faces == ():
        ret, f1 = vc.read()
        gray = cv2.cvtColor(f1,cv2.COLOR_BGR2GRAY)
        faces = fc.detectMultiScale(gray,scaleFactor = 1.1,minNeighbors=5,minSize=(30,30),)
    
        for(x1,y1,w1,h1) in faces:
            cv2.rectangle(f1,(x1,y1),(x1+w1,y1+h1),(0,255,0),2)
        cv2.imshow('Video',f1)
        key = cv2.waitKey(1)
        if key== ord('q'):
            break
    print(f1)
    f1 = f1[:,:,0]
    f3 = f1[y1:y1+h1,x1:x1+w1]
    Image.fromarray(f3).save("f3.jpg")
    vc.release()
    cv2.destroyAllWindows()


def log():
    fc1 = cv2.CascadeClassifier(cascpath)
    faces1 = ()
    vc1 = cv2.VideoCapture(0)
    while faces1 == ():
        ret1,f2 = vc1.read()
        gray = cv2.cvtColor(f2,cv2.COLOR_BGR2GRAY)
        faces1 = fc1.detectMultiScale(
        gray,scaleFactor=1.1,minNeighbors=5,minSize=(30,30))
        for (x2,y2,w2,h2) in faces1:
            cv2.rectangle(f2,(x2,y2),(x2+w2,y2+h2),(0,255,0),2)
        cv2.imshow('video',f2)
        key = cv2.waitKey(1)
        if key==ord('q'):
            break
    f2 = f2[:,:,0]
    f4 = f2[y2:y2+h2,x2:x2+w2]
    Image.fromarray(f4).save("f4.jpg")
    vc1.release()
    # print(faces1)
    cv2.destroyAllWindows()
    return check()

print('''
--------------------------------------------
|Welcome to Face Verification Login System  |
--------------------------------------------
    1) Press 1 for Registration             |
    2) Press 2 for Login                    |
    3) Press 3 to Exit                      |
--------------------------------------------
''')
while True:
    take_in = int(input("Enter: "))
    if take_in==1:
        reg()
        print("Registered Successfully")
    elif take_in==2:
        res = log()
        if res[0]==True:
            print("Logged In Successfully ☺️")
            sys.exit(0)
        else:
            print("Face Not Recognised")
    else:
        print("Bye!!!")
        sys.exit(0)

