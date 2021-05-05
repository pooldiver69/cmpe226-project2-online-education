from flask import Blueprint, request, render_template, make_response
from . import cnx
import hashlib
import itertools

content = Blueprint('content', __name__, url_prefix='/content')

@content.route('')
def list_course():
    c_id = request.args.get("c_id")
    episode_number = request.args.get("episode_number")
    cursor = cnx.cursor(dictionary=True)
    query = ("""SELECT *
            FROM content
            WHERE c_id = %(c_id)s AND episode_number = %(episode_number)s
            """)
    cursor.execute(query, {"c_id": c_id,"episode_number": episode_number})
    content = cursor.fetchone()
    cursor.close()
    return render_template('content.html', content=content)
