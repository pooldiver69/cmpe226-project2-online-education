# SJSU CMPE 226 Spring2021TEAM5
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
            FROM course_view
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

    # fetch review
    query = ("""SELECT *
            FROM review AS R 
            JOIN student AS S ON S.s_id = R.s_id
            WHERE c_id = %(c_id)s 
            """)
    cursor.execute(query, {"c_id": c_id})
    reviews = cursor.fetchall()
    reviews = [
        {**x, "created_time": x['created_time'].strftime('%m/%d/%Y')} for x in reviews]
    # fetch question
    query = ("""SELECT *
            FROM question AS Q
            LEFT JOIN answer AS A ON Q.q_id = A.q_id
            JOIN student AS S ON S.s_id = Q.s_id
            WHERE c_id = %(c_id)s 
            """)
    cursor.execute(query, {"c_id": c_id})
    questions = cursor.fetchall()
#     print(questions)
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

    return render_template('course.html', contents=contents, reviews=reviews, questions=questions, purchase_url=purchase_url, c_id=c_id)


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

@course.route("/search")
def search_coruse():
    term = request.args.get("search")
    cursor = cnx.cursor(dictionary=True)
    query = ("""SELECT *
            FROM course_view
            WHERE courseName LIKE %(term)s
            """)
    cursor.execute(query, {"term": '%' + term + '%'})
    r = cursor.fetchall()
    courses = [
        {**x, "c_url": "http://127.0.0.1:5000/course/" + str(x["c_id"])} for x in r]
    cursor.close()
    return render_template('course_list.html', courses=courses)
