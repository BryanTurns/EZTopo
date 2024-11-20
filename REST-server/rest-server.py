from flask import Flask

app = Flask(__name__)


@app.route("/api/uploadVideo")
def chop_video():
    return "<p>Uploading</p>"

@app.route("/api/checkStatus")
def check_status():
    return "Checking status"

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

