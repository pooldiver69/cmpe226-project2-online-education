from flask import Blueprint, request
from . import cnx
import hashlib

auth = Blueprint('auth', __name__, url_prefix='/auth')

__AUTH_SALT__ = "cmpe226"

@auth.route("/signup", methods=['POST'])
def signup():
    # print(request.form)
    if request.form['psw'] != request.form['psw-repeat']:
        return "password does not match!"
    hashed_psw = hashlib.md5((request.form['psw'] + __AUTH_SALT__).encode())
    cursor = cnx.cursor()
    query = ("""SELECT * FROM auth
            WHERE email = %(email)s""")
    cursor.execute(query, {"email": request.form['email']})
    if cursor.fetchone():
        return "email already in used!"
    cursor.close()
    cursor = cnx.cursor()
    create_auth = ("INSERT INTO auth "
                "(email, pwd) "
                "VALUES (%(email)s, %(pwd)s)")
    cursor.execute(create_auth, {"email": request.form['email'], "pwd":  hashed_psw.hexdigest()})
    user_id = cursor.lastrowid
    create_student = ("INSERT INTO student "
                "(s_name, user_id) "
                "VALUES (%(s_name)s, %(user_id)s)")
    cursor.execute(create_student, {"s_name": request.form['name'], "user_id":  user_id})
    print (cursor.lastrowid)
    cnx.commit()
    cursor.close()

    return "Signed up!"


@auth.route("/signin", methods=['POST'])
def signin():
    # print(request.form)
    hashed_psw = hashlib.md5((request.form['psw'] + __AUTH_SALT__).encode())
    cursor = cnx.cursor()
    query = ("""SELECT * FROM auth
            WHERE email = %(email)s""")
    cursor.execute(query, {"email": request.form['email']})
    r = cursor.fetchone()
    if not r:
        return "login info not correct"
    print(r)
    if r[-1] != hashed_psw.hexdigest():
        return "login info not correct"
    query = ("""SELECT * FROM student
            WHERE user_id = %(user_id)s""")
    cursor.execute(query, {"user_id": r[0]}) 
    r = cursor.fetchone()     
    cursor.close()

    return "welcome back, "+ r[1]
