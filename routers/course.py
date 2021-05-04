from flask import Blueprint, request, render_template, make_response
from . import cnx
import hashlib

course = Blueprint('course', __name__, url_prefix='/course')

@course.route('')
def list_course():
    cursor = cnx.cursor()
    query = ("""SELECT * FROM course""")
    cursor.execute(query)
    r = cursor.fetchall()
    for x in list(r):
        print(x)
    cursor.close()
    return render_template('course_list.html')