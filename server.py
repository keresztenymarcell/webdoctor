from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import data_handler, connection
import time
import os

DIRNAME = os.path.dirname(__file__)
UPLOAD_FOLDER_QUESTIONS = DIRNAME + "/static/pictures/question_pictures/"
UPLOAD_FOLDER_ANSWERS = DIRNAME + "/static/pictures/answer_pictures/"


app = Flask(__name__)


@app.route("/")
@app.route("/list")
def list_page():

    # new sorting
    order_by = request.args.get('order_by')
    order_direction = request.args.get('order_direction')
    questions = data_handler.get_all_data('question', order_by, order_direction)

    # old
    # questions = data_handler.sort_data(connection.DATA_FILE_PATH_QUESTIONS, order_by, order_direction)

    return render_template('list.html', header=data_handler.QUESTIONS_HEADER, keys=connection.QUESTION_KEYS,
                           questions=questions, orderby=order_by, orderdir=order_direction)


@app.route("/question/<question_id>")
def display_question(question_id):
    # questions = data_handler.get_all_questions()
    questions = connection.open_csvfile(connection.DATA_FILE_PATH_QUESTIONS)
    answers = data_handler.sort_data(connection.DATA_FILE_PATH_ANSWERS, "vote_number", "desc")
    if request.method == "GET":
        for question in questions:
            if question["id"] == question_id:
                question["view_number"] = int(question["view_number"]) + 1
                connection.write_files(connection.DATA_FILE_PATH_QUESTIONS, connection.QUESTION_KEYS, questions)
                return render_template('display_question.html', question=question, answers=answers)


@app.route("/add-question", methods=["GET", "POST"])
def write_questions():
    questions = connection.open_csvfile(connection.DATA_FILE_PATH_QUESTIONS)
    new_question_id = data_handler.generate_id(questions)
    if request.method == "POST":

        get_data = request.form.to_dict()

        if secure_filename(request.files['image'].filename) != "":
            get_data["image"] = secure_filename(request.files['image'].filename)
            folder_route = UPLOAD_FOLDER_QUESTIONS + get_data["image"]
            request.files["image"].save(folder_route)

        # function to add the question, I dont know exactly how to add image route yet.
        # data_handler.add_new_question(get_data)

        questions.append(get_data)
        connection.write_files(connection.DATA_FILE_PATH_QUESTIONS,connection.QUESTION_KEYS,questions)
        return redirect(url_for("display_question", question_id=get_data["id"]))

    return render_template('question.html')


@app.route("/question/<question_id>/edit", methods=["GET", "POST"])
def edit_question(question_id):
    questions = connection.open_csvfile(connection.DATA_FILE_PATH_QUESTIONS)
    if request.method == 'POST':

        edited_question = request.form.to_dict()
        
        # new edit function
        # data_handler.edit_question(question_id, edited_question)

        # old one
        data_handler.edit_database(questions, edited_question, question_id)
        return redirect(url_for("display_question", question_id=question_id))

    # SQL
    # target_question = data_handler.get_question_by_id(question_id)

    target_question = data_handler.find_data(questions, question_id)
    if target_question is None:
        return redirect(url_for("display_question", question_id=question_id))
    return render_template("question.html", question=target_question)


@app.route("/question/<question_id>/delete")
def delete_question(question_id):
    data_handler.delete_question_by_id(question_id)
    return redirect("/list")


@app.route("/answer/<answer_id>/delete")
def delete_answer(answer_id):
    answers = connection.open_csvfile(connection.DATA_FILE_PATH_ANSWERS)
    target_answer = data_handler.find_data(answers, answer_id)
    question_id = target_answer["question_id"]
    data_handler.delete_answer_by_id(answer_id)
    return redirect(f'/question/{question_id}')


@app.route("/question/<question_id>/vote_up")
def question_vote_up(question_id):
    questions = connection.open_csvfile(connection.DATA_FILE_PATH_QUESTIONS)
    target_question = data_handler.find_data(questions, question_id)
    target_question["vote_number"] = int(target_question["vote_number"]) + 1
    data_handler.edit_database(questions, target_question, question_id)
    return redirect("/list")


@app.route("/question/<question_id>/vote_down")
def question_vote_down(question_id):
    questions = connection.open_csvfile(connection.DATA_FILE_PATH_QUESTIONS)
    target_question = data_handler.find_data(questions, question_id)
    target_question["vote_number"] = int(target_question["vote_number"]) - 1
    data_handler.edit_database(questions, target_question, question_id)
    return redirect("/list")


@app.route("/question/<question_id>/new_answer", methods= ["GET", "POST"])
def add_new_answer(question_id):
    answers = connection.open_csvfile(connection.DATA_FILE_PATH_ANSWERS)
    new_answer_id = data_handler.generate_id(answers)

    if request.method == "POST":
        get_data = request.form.to_dict()
        get_data["id"] = new_answer_id
        get_data["submission_time"] = time.time()
        get_data["vote_number"] = 0
        get_data["question_id"] = question_id

        if secure_filename(request.files['image'].filename) != "":
            get_data["image"] = secure_filename(request.files['image'].filename)
            folder_route = UPLOAD_FOLDER_ANSWERS + get_data["image"]
            request.files["image"].save(folder_route)
        answers.append(get_data)
        connection.write_files(connection.DATA_FILE_PATH_ANSWERS, connection.ANSWER_KEYS, answers)

        return redirect(url_for("display_question", question_id=question_id))

    return render_template('add_new_answer.html', question_id=question_id)


@app.route("/answer/<answer_id>/vote_up")
def answer_vote_up(answer_id):
    answers = connection.open_csvfile(connection.DATA_FILE_PATH_ANSWERS)
    target_answer = data_handler.find_data(answers, answer_id)
    target_answer["vote_number"] = int(target_answer["vote_number"]) + 1
    question_id = target_answer["question_id"]
    data_handler.edit_database(answers, target_answer, answer_id)
    return redirect(f'/question/{question_id}')


@app.route("/answer/<answer_id>/vote_down")
def answer_vote_down(answer_id):
    answers = connection.open_csvfile(connection.DATA_FILE_PATH_ANSWERS)
    target_answer = data_handler.find_data(answers, answer_id)
    target_answer["vote_number"] = int(target_answer["vote_number"]) - 1
    question_id = target_answer["question_id"]
    data_handler.edit_database(answers, target_answer, answer_id)
    return redirect(f'/question/{question_id}')


if __name__ == "__main__":
    app.run(
        debug=True,
    )
