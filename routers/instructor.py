# SJSU CMPE 226 Spring2021TEAM5
from flask import Blueprint, request, render_template, make_response, redirect, flash
import os
from werkzeug.utils import secure_filename
from . import cnx, auth_checker
import hashlib
import itertools
import datetime
import time
instructor_portal = Blueprint('instructor_portal', __name__, url_prefix='/instructor_portal')


@instructor_portal.route('')
def list_my_course():
    i_id = request.cookies.get('i_id')
    if not i_id:
        flash('You have no access to this resource')
        return redirect("/")
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
    i_id = request.cookies.get("i_id")
    if not i_id:
        flash('You have no access to this resource')
        return redirect('/')
    cursor = cnx.cursor(dictionary=True)
    create_course = ("INSERT INTO course "
                "(c_name, c_description, subject, price, author_id) "
                "VALUES (%(c_name)s, %(c_description)s,%(subject)s, %(price)s, %(author_id)s)")
    cursor.execute(create_course, {"c_name": request.form['name'], "c_description": request.form['description'], "subject": request.form['subject'],
                   "price": request.form['price'], "author_id": i_id})
    cnx.commit()
    cursor.close()
    return redirect('/instructor_portal')

@instructor_portal.route('/course/<c_id>', methods=['GET'])
def get_single_course(c_id):
    i_id = request.cookies.get("i_id")
    if not i_id:
        return redirect('/')
    cursor = cnx.cursor(dictionary=True)

    # query if i_id teach this course
    query = ("""SELECT *
            FROM course
            WHERE author_id = %(i_id)s and c_id = %(c_id)s 
            """)
    cursor.execute(query, {"i_id": i_id, "c_id": c_id})
    course = cursor.fetchone()
    # print(course)
    if not course:
        flash('You have no access to this resource')
        return redirect("/")
    #query content info
    query = ("""SELECT *
            FROM content
            WHERE c_id = %(c_id)s 
            """)
    cursor.execute(query, {"c_id": c_id})
    r = cursor.fetchall()
    contents = [{**x, "content_url": "http://127.0.0.1:5000/instructor_portal/content?c_id=" +
                 str(x["c_id"]) + '&episode_number=' + str(x['episode_number'])} for x in r]

    query = ("""SELECT *
            FROM question AS Q
            JOIN student AS S ON Q.s_id = S.s_id 
            WHERE c_id = %(c_id)s AND resolved = %(resolved)s
            """)
    cursor.execute(query, {"c_id" :c_id, "resolved": False})
    unsolved_questions = cursor.fetchall()
    print(unsolved_questions)
    cursor.close()
    return render_template('instructor_course.html', contents=contents, course=course, unsolved_questions=unsolved_questions)


@instructor_portal.route('/update/course/<c_id>', methods=['POST'])
def update_single_course(c_id):
    i_id = request.cookies.get("i_id")
    if not i_id:
        return redirect('/')
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
    
    #update course
    data = request.form
    update_str = ""
    # print(data)
    for item in enumerate(data):
        _, key = item
        val = data[key]
        update_str += (str(key)  + "= '" + str(val) + "', ")
    update_str = update_str[:-2]
    updates = ("""UPDATE course
            SET {}
            WHERE c_id = %(c_id)s 
            """.format(update_str))
    cursor.execute(updates, {"c_id": c_id})
    cursor.close()
    return redirect('/instructor_portal/course/' + c_id)

@instructor_portal.route('/content')
def get_signle_content():
    c_id = request.args.get("c_id")
    episode_number = request.args.get("episode_number")
    i_id = request.cookies.get("i_id")
    if not i_id:
        return redirect('/')
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
        return redirect('/instructor_portal')

    query = ("""SELECT *
            FROM content
            WHERE c_id = %(c_id)s AND episode_number = %(episode_number)s
            """)
    cursor.execute(query, {"c_id": c_id, "episode_number": episode_number})
    content = cursor.fetchone()
    cursor.close()
    return render_template('instructor_content.html', content=content)


@instructor_portal.route('/update/content', methods=['POST'])
def update_single_content():
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
        flash("you have no access to this resource")
        return redirect('/')
    
    #update course
    data = request.form
    update_str = ""
    # print(data)
    for item in enumerate(data):
        _, key = item
        val = data[key]
        update_str += (str(key)  + "= '" + str(val) + "', ")
    update_str = update_str[:-2]
    updates = ("""UPDATE content
            SET {}
            WHERE c_id = %(c_id)s AND episode_number = %(episode_number)s
            """.format(update_str))
    cursor.execute(updates, {"c_id": c_id, "episode_number": episode_number})
    cursor.close()
    return redirect('/instructor_portal/content?c_id=' + c_id +"&episode_number=" + episode_number)


ALLOWED_EXTENSIONS = ['mp4']
__UPLOAD_FOLDER__ = '/static/'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@instructor_portal.route('/upload/content', methods=['POST'])
def upload_file():
    if request.method == 'POST':
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
            flash("you have no access to this resource")
            return redirect('/')

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('File Uploading failed')
            return redirect('/instructor_portal/content?c_id=' + c_id +"&episode_number=" + episode_number)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect('/instructor_portal/content?c_id=' + c_id +"&episode_number=" + episode_number)
        if file and allowed_file(file.filename):
            filename = secure_filename(str(time.time_ns()) + "." +file.filename.rsplit('.', 1)[1].lower())
            filepath = os.path.abspath("./" + __UPLOAD_FOLDER__+filename)
            file.save(filepath)
            updates = ("""UPDATE content
                    SET stored_loc = %(stored_loc)s
                    WHERE c_id = %(c_id)s AND episode_number = %(episode_number)s
                    """)
            cursor.execute(updates, {"c_id": c_id, "episode_number": episode_number, "stored_loc": filename})
            cursor.close()
            return redirect('/instructor_portal/content?c_id=' + c_id +"&episode_number=" + episode_number)


@instructor_portal.route('/create/content', methods=['POST'])
def create_content():

    i_id = request.cookies.get("i_id")
    if not i_id:
        flash('You have no access to this resource')
        return redirect('/')

    cursor = cnx.cursor(dictionary=True)

    begin_transaction = ("START TRANSACTION")
    cursor.execute(begin_transaction)

    savePoint1 = ("SAVEPOINT point1")
    cursor.execute(savePoint1)

    title_query = ("""select title
                    from content
                    where c_id = %(c_id)s
    """)
    cursor.execute(title_query, {"c_id": request.form['c_id']})
    titles = cursor.fetchall()

    create_content = ("INSERT INTO content "
                "(c_id, title, stored_loc, con_description) "
                "VALUES (%(c_id)s, %(title)s, %(stored_loc)s, %(con_description)s)")
    cursor.execute(create_content, {"c_id": request.form['c_id'], "title": request.form['title'],
                    "stored_loc": '', "con_description": request.form['con_description']})
    episode_number = cursor.lastrowid


    if {'title': request.form['title']} in titles:
        rollback = "ROLLBACK TO SAVEPOINT point1"
        cursor.execute(rollback)
        #  print("cannot add !!!!!!!!!!!")
        flash("content title already exists")
        return redirect("/instructor_portal/course/" + request.form['c_id'])
    else:
        commit = "COMMIT"
        cursor.execute(commit)

        cnx.commit()
        cursor.close()

        return redirect('/instructor_portal/content?c_id=' + request.form['c_id'] +"&episode_number=" + str(episode_number))

@instructor_portal.route('/answer', methods=['POST'])
def answer_question():
    i_id = request.cookies.get("i_id")
    if not i_id:
        flash('You have no access to this resource')
        return redirect('/')

    cursor = cnx.cursor(dictionary=True)
    begin_transaction = ("START TRANSACTION")
    cursor.execute(begin_transaction)

    savePoint1 = ("SAVEPOINT point1")
    cursor.execute(savePoint1)

    create_content = ("INSERT INTO answer "
                "(q_id, i_id, a_message, a_created_time) "
                "VALUES (%(q_id)s, %(i_id)s, %(a_message)s, %(a_created_time)s)")
    cursor.execute(create_content, {"q_id": request.form['q_id'], "i_id": i_id,
                    "a_message": request.form['a_message'], "a_created_time": datetime.datetime.utcnow()}) 

    updates = ("""UPDATE question
            SET resolved ='1'
            WHERE q_id = %(q_id)s 
            """)
    cursor.execute(updates, {"q_id": request.form['q_id']})

    if not cursor.rowcount:
        rollback = "ROLLBACK TO SAVEPOINT point1"
        cursor.execute(rollback)
        #  print("cannot add !!!!!!!!!!!")
        flash("answer submit failed")
    cnx.commit()
    cursor.close()
    return redirect('/instructor_portal/course/' + request.form['c_id'])

@instructor_portal.route('/delete/content', methods=['POST'])
def delete_content():
    c_id = request.form["c_id"]
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
        flash("you have no access to this resource")
        return redirect('/')

    delete_content = ("DELETE FROM content "
                "WHERE c_id = %(c_id)s AND episode_number = %(episode_number)s  ")
    cursor.execute(delete_content, {"c_id": c_id, "episode_number": request.form['episode_number']})
    cnx.commit()
    cursor.close()
    return redirect('/instructor_portal/course/' + c_id)