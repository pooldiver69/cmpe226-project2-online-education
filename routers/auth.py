from flask import Blueprint, request
from . import cnx
auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route("/signup", methods=['POST'])
def signup():
    print(request.form)
    return "get it"