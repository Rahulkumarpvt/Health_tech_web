import mysql.connector
import getpass
from cryptography.fernet import Fernet
import sys


db_obj = mysql.connector.connect(
        host = "localhost",
        user = "root",
        passwd = getpass.getpass(prompt = "Password: "),
        database = "face_login")
my_cursor = db_obj.cursor(buffered=True)
my_cursor.execute('select reg_pic from user_data where u_id=%s',(0,))
res = my_cursor.fetchall()
k = res[0][0]

def en(pic_name):
    fernet = Fernet(k)
    pic_name = fernet.encrypt(pic_name.encode())
    return pic_name

def dc(pic_name):
    fernet = Fernet(k)
    pic_name = fernet.decrypt(pic_name.encode()).decode()
    return pic_name

def db_insert(username,pic_name,count):
    try:
        q = 'insert into user_data values(%s,%s,%s)'
        pic_name = en(pic_name)
        v = (count,username,pic_name)
        my_cursor.execute(q,v)
        db_obj.commit()
        return 1
    except:
        return 0
def load(username):
    try:
        my_cursor.execute('select reg_pic from user_data where u_name=%s',(username,))
        pic_name = my_cursor.fetchall()
        pic_name = pic_name[0][0]
        return dc(pic_name)
    except:
        print("User Not Registered !!")
        sys.exit(0)
   












# key = Fernet.generate_key()
# print(key)
# my_cursor.execute("create database face_login")
# my_cursor.execute("show tables")
# for i in my_cursor:
#     print(i)
# q = 'insert into user_data values(%s,%s,%s)'
# v = (1,'KEY',key)
# my_cursor.execute(q,v)
# db_obj.commit()

