from flask import Blueprint, request, render_template, make_response, redirect
from . import cnx, auth_checker
import hashlib
import itertools
import datetime
course = Blueprint('course', __name__, url_prefix='/course')


@course.route('')
def list_course():
    cursor = cnx.cursor(dictionary=True)
    query = ("""SELECT *
            FROM course AS C 
            JOIN instructor AS I ON C.author_id = I.i_id
            """)
    cursor.execute(query)
    r = cursor.fetchall()
    courses = [
        {**x, "c_url": "http://127.0.0.1:5000/course/" + str(x["c_id"])} for x in r]
    cursor.close()
    return render_template('course_list.html', courses=courses)


@course.route('/<c_id>', methods=['GET'])
def get_single_course(c_id):
    i_id = request.cookies.get("i_id")
    cursor = cnx.cursor(dictionary=True)

    # query if i_id teach this course
    query = ("""SELECT *
            FROM course
            WHERE author_id = %(i_id)s and c_id = %(c_id)s 
            """)
    cursor.execute(query, {"i_id": i_id, "c_id": c_id})
    course = cursor.fetchone()

    #query content info
    query = ("""SELECT *
            FROM content
            WHERE c_id = %(c_id)s 
            """)
    cursor.execute(query, {"c_id": c_id})
    r = cursor.fetchall()
    contents = [{**x, "content_url": "http://127.0.0.1:5000/content?c_id=" +
                 str(x["c_id"]) + '&episode_number=' + str(x['episode_number'])} for x in r]
    s_id = request.cookies.get("s_id")
    purchase_url = ""

    # check purchase only not teaching this course and valid student
    if s_id and not course:
        query = ("""SELECT *
                FROM purchase
                WHERE c_id = %(c_id)s AND s_id = %(s_id)s
                """)
        cursor.execute(query, {"c_id": c_id, "s_id": s_id})
        r = cursor.fetchone()
        if not r:
            purchase_url = "http://127.0.0.1:5000/course/purchase/" + c_id
    cursor.close()
    return render_template('course.html', contents=contents, purchase_url=purchase_url)


@course.route('/purchase/<c_id>', methods=['GET'])
def purchase_single_course(c_id):
    s_id = request.cookies.get("s_id")
    if not auth_checker(request):
        return redirect('/auth')
    cursor = cnx.cursor(dictionary=True)
    query = ("""SELECT *
            FROM course AS C 
            WHERE c_id = %(c_id)s
            """)
    cursor.execute(query, {"c_id": c_id})
    course = cursor.fetchone()
    purchase = ("INSERT INTO purchase "
                "(c_id, s_id, p_price, purchsed_time) "
                "VALUES (%(c_id)s, %(s_id)s,%(p_price)s, %(purchsed_time)s)")
    cursor.execute(purchase, {"c_id": c_id, "s_id": s_id,
                   "p_price": course['price'], "purchsed_time": datetime.datetime.utcnow()})
    cnx.commit()
    cursor.close()
    return redirect('/course/' + c_id)
