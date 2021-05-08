from flask import Flask, request, render_template
from routers.auth import auth
from routers.course import course
from routers.content import content
from routers.instructor import instructor_portal
from routers.student import student_portal
app = Flask(__name__, static_folder='static')
app.secret_key = 'cmpe226'

app.register_blueprint(auth)
app.register_blueprint(course)
app.register_blueprint(content)
app.register_blueprint(instructor_portal)
app.register_blueprint(student_portal)
@app.route('/')
def hello():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

