# SJSU CMPE 226 Spring2021TEAM5
from flask import Blueprint, request, render_template, make_response, redirect
from . import cnx, auth_checker
import hashlib
import itertools

content = Blueprint('content', __name__, url_prefix='/content')


@content.route('')
def get_signle_content():
    if not auth_checker(request):
        return redirect('/auth')
    c_id = request.args.get("c_id")
    episode_number = request.args.get("episode_number")
    i_id = request.cookies.get("i_id")
    s_id = request.cookies.get("s_id")
    course = None
    cursor = cnx.cursor(dictionary=True)
    # query if i_id teach this course
    if i_id:
        query = ("""SELECT *
                FROM course
                WHERE author_id = %(i_id)s and c_id = %(c_id)s 
                """)
        cursor.execute(query, {"i_id": i_id, "c_id": c_id})
        course = cursor.fetchone()
    if not course:
        query = ("""SELECT *
                FROM purchase
                WHERE s_id = %(s_id)s and c_id = %(c_id)s  
                """)
        cursor.execute(query, {"s_id": s_id, "c_id": c_id})
        course = cursor.fetchone()
    if not course:
        return redirect('/course/' + c_id)

    query = ("""SELECT *
            FROM content
            WHERE c_id = %(c_id)s AND episode_number = %(episode_number)s
            """)
    cursor.execute(query, {"c_id": c_id, "episode_number": episode_number})
    content = cursor.fetchone()
    cursor.close()
    return render_template('content.html', content=content)
