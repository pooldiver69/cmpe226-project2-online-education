from flask import render_template
def auth_checker(request):
    if not request.cookies.get('user_id'):
        return False
    else:
        return True