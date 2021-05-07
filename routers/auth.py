from flask import Blueprint, request, render_template, make_response
from . import cnx
import hashlib

auth = Blueprint('auth', __name__, url_prefix='/auth')

__AUTH_SALT__ = "cmpe226"


@auth.route('')
def hello():
    return render_template('auth.html')


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
    cursor.execute(
        create_auth, {"email": request.form['email'], "pwd":  hashed_psw.hexdigest()})
    user_id = cursor.lastrowid
    create_student = ("INSERT INTO student "
                      "(s_name, user_id) "
                      "VALUES (%(s_name)s, %(user_id)s)")
    cursor.execute(create_student, {
                   "s_name": request.form['name'], "user_id":  user_id})
    sid = cursor.lastrowid
    cnx.commit()
    cursor.close()
    resp = make_response(render_template('index.html'))
    resp.set_cookie('user_id', str(user_id))
    resp.set_cookie('s_id', str(sid))
    return resp


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
    user_id = r[0]
    if r[-1] != hashed_psw.hexdigest():
        return "login info not correct"
    query = ("""SELECT * FROM student
            WHERE user_id = %(user_id)s""")
    cursor.execute(query, {"user_id": user_id})
    r = cursor.fetchone()
    resp = make_response(render_template('index.html'))
    resp.set_cookie('user_id', str(user_id))
    resp.set_cookie('s_id', str(r[0]))

    # set i_id 
    query = ("""SELECT * FROM instructor
            WHERE user_id = %(user_id)s""")
    cursor.execute(query, {"user_id": user_id})
    r = cursor.fetchone()
    if r:
        resp.set_cookie('i_id', str(r[0]))
    cursor.close()
    return resp


@auth.route("/signout")
def signout():
    resp = make_response(render_template('index.html'))
    resp.set_cookie('user_id', expires=0)
    resp.set_cookie('s_id', expires=0)
    resp.set_cookie('i_id', expires=0)
    return resp
