from flask import Blueprint, request

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route("/signup", methods=['POST'])
def signup():
    print(request.form)
    return "get it"