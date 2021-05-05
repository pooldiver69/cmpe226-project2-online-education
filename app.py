from flask import Flask, request, render_template
from routers.auth import auth
from routers.course import course
from routers.content import content

app = Flask(__name__, static_folder='static')

app.register_blueprint(auth)
app.register_blueprint(course)
app.register_blueprint(content)
@app.route('/')
def hello():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

