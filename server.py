from flask import Flask, render_template, request, redirect

import data_handler


app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/list")
def list_page():
    questions = data_handler.sort_questions(data_handler.DATA_FILE_PATH_questions, True)
    return render_template(list.html, data_handler.QUESTIONS_HEADER, questions)


if __name__ == "__main__":
    app.run()
