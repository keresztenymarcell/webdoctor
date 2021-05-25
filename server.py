from flask import Flask, render_template, request, redirect

import data_handler, connection


app = Flask(__name__)


@app.route("/")
def hello():
    return 'Hello World'


@app.route("/list")
def list_page():
    order_by = request.args.get('order_by', 'submission_time')
    order_direction = request.args.get('order_direction', 'desc')
    questions = data_handler.sort_questions(order_by, order_direction)
    return render_template('list.html', header=data_handler.QUESTIONS_HEADER, keys=connection.QUESTION_KEYS, questions=questions)


@app.route("/questions/<question_id>")
def display_question(question_id):
    questions = connection.open_csvfile(connection.DATA_FILE_PATH_QUESTIONS)
    answers = connection.open_csvfile(connection.DATA_FILE_PATH_ANSWERS)

    if request.method == "GET":
        for question in questions:
            if question["id"] == question_id:
                return render_template('display_question.html', question=question, answers=answers)


if __name__ == "__main__":
    app.run(
        debug=True,
    )
