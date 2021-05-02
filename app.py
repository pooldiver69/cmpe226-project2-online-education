from flask import Flask, request, render_template
from routers.auth import auth

app = Flask(__name__)

app.register_blueprint(auth)

@app.route('/')
def hello():
    return render_template('auth.html')

if __name__ == '__main__':
    app.run(debug=True)

