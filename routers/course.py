from flask import Blueprint, request, render_template, make_response
from . import cnx
import hashlib
import itertools

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
    courses = [{**x, "c_url": "http://127.0.0.1:5000/course/" + str(x["c_id"])} for x in r]
    cursor.close()
    return render_template('course_list.html', courses=courses)

@course.route('/<c_id>', methods=['GET'])
def get_single_course(c_id):
    cursor = cnx.cursor(dictionary=True)
    query = ("""SELECT *
            FROM content 
            WHERE c_id = %(c_id)s
            """)
    cursor.execute(query, {"c_id": c_id})
    r = cursor.fetchall()
    contents = [{**x, "content_url": "http://127.0.0.1:5000/content?c_id=" + str(x["c_id"]) + '&episode_number=' + str(x['episode_number'])} for x in r]
    cursor.close() 
    return render_template('course.html', contents=contents)