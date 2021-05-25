from flask import Flask, render_template, request, redirect, url_for

import data_handler, connection
import time


app = Flask(__name__)


@app.route("/")
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


@app.route("/add-question", methods=["GET", "POST"])
def write_questions():
    questions = connection.open_csvfile(connection.DATA_FILE_PATH_QUESTIONS)
    if request.method == "POST":

        if questions is []:
            question_id = 0
        else:
            question_id = int(questions[-1]["id"]) + 1


        get_data = request.form.to_dict()
        get_data["id"] = str(question_id)
        get_data["submission_time"] = time.time()
        get_data["view_number"] = 0
        get_data["vote_number"] = 0
        questions.append(get_data)
        connection.write_files(connection.DATA_FILE_PATH_QUESTIONS,connection.QUESTION_KEYS,questions)
        return redirect(url_for("display_question", question_id=question_id))

    return render_template('question.html')


@app.route("/question/<question_id>/edit", methods=["GET", "POST"])
def edit_question(question_id):
    questions = connection.open_csvfile(connection.DATA_FILE_PATH_QUESTIONS)
    if request.method == 'POST':
        edited_question = request.form.to_dict()
        data_handler.edit_question(questions, edited_question, question_id)
        return redirect("/list")

    target_question = data_handler.find_question(questions, question_id)
    if target_question is None:
        return redirect("/list")
    return render_template("question.html", question=target_question)


@app.route("/question/<question_id>/delete")
def delete_question(question_id):
    data_handler.delete_question_by_id(question_id)
    return redirect(url_for("display_question", question_id=question_id))









if __name__ == "__main__":
    app.run(
        debug=True,
    )
