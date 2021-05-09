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

@student_portal.route('/review', methods=['POST'])
def post_review():
    s_id = request.cookies.get('s_id')
    if not s_id:
        flash('You have no access to this resource')
        return redirect("/")
    cursor = cnx.cursor(dictionary=True)
    query = ("""SELECT *
            FROM purchase
            WHERE s_id = %(s_id)s and c_id = %(c_id)s  
            """)
    cursor.execute(query, {"s_id": s_id, "c_id": request.form['c_id']})
    course = cursor.fetchone()
    if not course:
        flash("you don't have access to this access")
        return redirect('/course/' + request.form['c_id'])
    create_review = ("INSERT INTO review "
                "(c_id, s_id, star, r_message, created_time) "
                "VALUES (%(c_id)s, %(s_id)s, %(star)s, %(r_message)s, %(created_time)s)")
    cursor.execute(create_review, {"c_id": request.form['c_id'], "s_id": s_id, "star": request.form['star'],
                    "r_message": request.form['r_message'], "created_time": datetime.datetime.utcnow()})
    cnx.commit()
    cursor.close()
    return redirect('/course/' + request.form['c_id'])

@student_portal.route('/question', methods=['POST'])
def post_question():
    s_id = request.cookies.get('s_id')
    if not s_id:
        flash('You have no access to this resource')
        return redirect("/")
    cursor = cnx.cursor(dictionary=True)
    query = ("""SELECT *
            FROM purchase
            WHERE s_id = %(s_id)s and c_id = %(c_id)s  
            """)
    cursor.execute(query, {"s_id": s_id, "c_id": request.form['c_id']})
    course = cursor.fetchone()
    if not course:
        flash("you don't have access to this access")
        return redirect('/course/' + request.form['c_id'])
        
    create_review = ("INSERT INTO question "
                "(c_id, s_id, q_message, q_created_time, resolved) "
                "VALUES (%(c_id)s, %(s_id)s, %(q_message)s, %(q_created_time)s, %(resolved)s)")
    cursor.execute(create_review, {"c_id": request.form['c_id'], "s_id": s_id,
                    "q_message": request.form['q_message'], "q_created_time": datetime.datetime.utcnow(), "resolved":  False})
    cnx.commit()
    cursor.close()
    return redirect('/course/' + request.form['c_id'])