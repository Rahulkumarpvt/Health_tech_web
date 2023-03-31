import cv2
import sys
from PIL import Image
import face_recognition
import database

img_name = 'u'

with open('cnt','r') as f:
    count = f.read()
cap = cv2.VideoCapture(0)


def img_enc_dec(name_path):
    with open(name_path,'rb') as f:
        image = f.read()
    with open(name_path,'wb') as f:
        image = bytearray(image)
        for index,values in enumerate(image):
                image[index] = values ^ 12
        f.write(image)

def check(reg_pic):
    try:
        img_enc_dec("reg_img\\{}".format(reg_pic))
        img_enc_dec("reg_img\\Deml.jpg")
        known_image = face_recognition.load_image_file("reg_img\\{}".format(reg_pic))
        unknown_image = face_recognition.load_image_file("reg_img\\Deml.jpg")
    
        known_encode = face_recognition.face_encodings(known_image)[0]
        unknown_encode = face_recognition.face_encodings(unknown_image)[0]

        res = face_recognition.compare_faces([known_encode],unknown_encode)
        img_enc_dec("reg_img\\{}".format(reg_pic))

        return res
    except:
        print("Try Again!!")
        sys.exit(0)


def f_r():
    username = input("Enter Username: ")
    while True:
        ret, frame = cap.read()
        cv2.imshow('Camera', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    print(frame)
    iname = img_name+count+'.jpg'
    print(iname)
    Image.fromarray(frame).save("reg_img\\{}".format(iname))
    cap.release()
    cv2.destroyAllWindows()
    img_enc_dec("reg_img\\{}".format(iname))
    res = database.db_insert(username,iname,count)
    if res==0:
        print("Username Not Available!!")
    else:
        with open('cnt','w') as f:
            f.write(str(int(count)+1))
        print("Successfully Registered")


def f_r_l(reg_pic):
    while True:
        ret, frame = cap.read()
        cv2.imshow('Camera', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    print(frame)
    Image.fromarray(frame).save("reg_img\\Deml.jpg")
    cap.release()
    cv2.destroyAllWindows()
    img_enc_dec("reg_img\\Deml.jpg")
    return check(reg_pic)


print('''
--------------------------------------------
|Welcome to Face Verification Login System  |
--------------------------------------------
    1) Press 1 for Registration             |
    2) Press 2 for Login                    |
    3) Press 3 to Exit                      |
--------------------------------------------
''')
try:
    take_in = int(input("Enter: "))
    if take_in==1:
        f_r()
    elif take_in==2:
        username = input("Enter Username: ")
        reg_pic = database.load(username)
        print(reg_pic)
        r = f_r_l(reg_pic)
        if r[0]==True:
            print("Logged In, Welcome :)")
        else:
            print("Verification Failed!!")

    else:
        print("Bye!!!")
        sys.exit(0)
except:
    print("Try Again,")