from flask import Flask, render_template, request, redirect

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/list")
def list_page():
    return "Hello World!"


if __name__ == "__main__":
    app.run()
