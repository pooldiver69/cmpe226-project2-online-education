from flask import Blueprint, request, render_template, make_response, redirect
from . import cnx, auth_checker
import hashlib
import itertools
import datetime
instructor_portal = Blueprint('instructor_portal', __name__, url_prefix='/instructor_portal')


@instructor_portal.route('')
def list_my_course():
    i_id = request.cookies.get('i_id')
    cursor = cnx.cursor(dictionary=True)
    query = ("""SELECT *
            FROM course AS C 
            JOIN instructor AS I ON C.author_id = I.i_id 
            WHERE C.author_id = %(i_id)s 
            """)
    cursor.execute(query, {"i_id": i_id})
    r = cursor.fetchall()
    courses = [
        {**x, "c_url": "http://127.0.0.1:5000/instructor_portal/course/" + str(x["c_id"])} for x in r]
    cursor.close()
    return render_template('instructor_portal.html', courses=courses)

@instructor_portal.route('/create', methods=['POST'])
def create_course():
    i_id = request.cookies.get('i_id')
    cursor = cnx.cursor(dictionary=True)
    create_course = ("INSERT INTO course "
                "(c_name, c_description, subject, price, author_id) "
                "VALUES (%(c_name)s, %(c_description)s,%(subject)s, %(price)s, %(author_id)s)")
    cursor.execute(create_course, {"c_name": request.form['description'], "c_description": request.form['description'], "subject": request.form['subject'],
                   "price": request.form['price'], "author_id": i_id})
    cnx.commit()
    cursor.close()
    return redirect('/instructor_portal')

@instructor_portal.route('/course/<c_id>', methods=['GET'])
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
    if not course:
        return redirect('/instructor_portal')
    #query content info
    query = ("""SELECT *
            FROM content
            WHERE c_id = %(c_id)s 
            """)
    cursor.execute(query, {"c_id": c_id})
    r = cursor.fetchall()
    contents = [{**x, "content_url": "http://127.0.0.1:5000/content?c_id=" +
                 str(x["c_id"]) + '&episode_number=' + str(x['episode_number'])} for x in r]

    cursor.close()
    return render_template('instructor_course.html', contents=contents, course=course)