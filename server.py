from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import data_handler, connection
import time
import os


app = Flask(__name__)


@app.route("/")
@app.route("/list")
def list_page():
    order_by = request.args.get('order_by', 'submission_time')
    order_direction = request.args.get('order_direction', 'desc')
    questions = data_handler.sort_questions(order_by, order_direction)
    return render_template('list.html', header=data_handler.QUESTIONS_HEADER, keys=connection.QUESTION_KEYS, questions=questions)


@app.route("/question/<question_id>")
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
        get_data["image"] = secure_filename(request.files['image'].filename)

        image_file = request.files['image']
        image_file.save(os.path.join(data_handler.UPLOAD_FOLDER_QUESTIONS, secure_filename(image_file.filename)))

        questions.append(get_data)
        connection.write_files(connection.DATA_FILE_PATH_QUESTIONS,connection.QUESTION_KEYS,questions)
        return redirect(url_for("display_question", question_id=question_id))

    return render_template('question.html')


@app.route("/question/<question_id>/edit", methods=["GET", "POST"])
def edit_question(question_id):
    questions = connection.open_csvfile(connection.DATA_FILE_PATH_QUESTIONS)
    if request.method == 'POST':
        edited_question = request.form.to_dict()
        data_handler.edit_questions(questions, edited_question, question_id)
        return redirect(url_for("display_question", question_id=question_id))

    target_question = data_handler.find_question(questions, question_id)
    if target_question is None:
        return redirect(url_for("display_question", question_id=question_id))
    return render_template("question.html", question=target_question)


@app.route("/question/<question_id>/delete")
def delete_question(question_id):
    data_handler.delete_question_by_id(question_id)
    return redirect("/list")


@app.route("/answer/<answer_id>/delete")
def delete_answer(answer_id):
    data_handler.delete_answer_by_id(answer_id)
    return redirect(url_for("display_question", question_id=question_id))


@app.route("/question/<question_id>/vote_up")
def question_vote_up(question_id):
    questions = connection.open_csvfile(connection.DATA_FILE_PATH_QUESTIONS)
    target_question = data_handler.find_question(questions, question_id)
    target_question["vote_number"] = int(target_question["vote_number"]) + 1
    data_handler.edit_questions(questions, target_question, question_id)
    return redirect("/list")


@app.route("/question/<question_id>/vote_down")
def question_vote_down(question_id):
    questions = connection.open_csvfile(connection.DATA_FILE_PATH_QUESTIONS)
    target_question = data_handler.find_question(questions, question_id)
    target_question["vote_number"] = int(target_question["vote_number"]) - 1
    data_handler.edit_questions(questions, target_question, question_id)
    return redirect("/list")


@app.route("/question/<question_id>/new_answer", methods= ["GET", "POST"])
def add_new_answer(question_id):
    questions = connection.open_csvfile(connection.DATA_FILE_PATH_QUESTIONS)
    answers = connection.open_csvfile(connection.DATA_FILE_PATH_ANSWERS)

    if not answers:
        new_id = 0
    else:
        new_id = int(answers[-1]["id"]) + 1

    ANSWER_KEYS = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']

    if request.method == "POST":
        for question in questions:
            if question["id"] is question_id:
                
                get_data = request.form.to_dict()
                get_data["id"] = new_id
                get_data["submission_time"] = time.time()
                get_data["vote_number"] = 0
                get_data["question_id"] = question_id
        answers.append(get_data)
        connection.write_files(connection.DATA_FILE_PATH_ANSWERS, connection.ANSWER_KEYS, answers)

        return redirect(url_for("display_question", question_id=question_id))

    return render_template('add_new_answer.html', question_id=question_id)


if __name__ == "__main__":
    app.run(
        debug=True,
    )
