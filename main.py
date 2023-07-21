from flask import Flask,render_template

app = Flask(__name__)

@app.route("/")
def hello_world():
    name = "Vincent"
    return render_template('hello.html', name=name)