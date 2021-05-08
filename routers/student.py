from flask import Blueprint, request, render_template, make_response, redirect, flash
from . import cnx, auth_checker
import hashlib
import itertools
import datetime
student_portal = Blueprint('student_portal', __name__, url_prefix='/student_portal')


@student_portal.route('')
def list_purchased_course():
    s_id = request.cookies.get('s_id')
    if not s_id:
        flash('You have no access to this resource')
        return redirect("/")
    cursor = cnx.cursor(dictionary=True)
    query = ("""SELECT *
            FROM purchase AS P 
            JOIN course AS C ON C.c_id = P.c_id 
            JOIN instructor AS I ON C.author_id = I.i_id
            WHERE P.s_id = %(s_id)s 
            """)
    cursor.execute(query, {"s_id": s_id})
    r = cursor.fetchall()
    # print(r[0])
    courses = [
        {**x, "c_url": "http://127.0.0.1:5000/course/" + str(x["c_id"]), "purchsed_time": x['purchsed_time'].strftime('%m/%d/%Y')} for x in r]
    cursor.close()
    return render_template('student_portal.html', courses=courses)