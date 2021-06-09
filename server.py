from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import data_handler, asd
import time
import os


DIRNAME = os.path.dirname(__file__)
UPLOAD_FOLDER_QUESTIONS = DIRNAME + "/static/pictures/question_pictures/"
UPLOAD_FOLDER_ANSWERS = DIRNAME + "/static/pictures/answer_pictures/"


app = Flask(__name__)


@app.route("/")
def main_page():
    return render_template("index.html")


@app.route("/list")
def list_page():

    # new sorting
    order_by = request.args.get('order_by', 'submission_time')
    order_direction = request.args.get('order_direction', 'desc')
    questions = data_handler.get_all_data('question', order_by, order_direction)

    # old
    # questions = data_handler.sort_data(connection.DATA_FILE_PATH_QUESTIONS, order_by, order_direction)

    return render_template('list.html', header=data_handler.QUESTIONS_HEADER, keys=data_handler.QUESTION_KEYS,
                           questions=questions, orderby=order_by, orderdir=order_direction)


@app.route("/question/<question_id>")
def display_question(question_id):

    question = data_handler.get_question_by_id(question_id)[0]
    answers = data_handler.get_all_data("answer", "vote_number", "desc")
    data_handler.increment_view_number(question_id)

    return render_template('display_question.html', question=question, answers=answers)


@app.route("/add-question", methods=["GET", "POST"])
def write_questions():

    if request.method == "POST":

        get_data = request.form.to_dict()

        if secure_filename(request.files['image'].filename) != "":
            get_data["image"] = secure_filename(request.files['image'].filename)
            folder_route = UPLOAD_FOLDER_QUESTIONS + get_data["image"]
            request.files["image"].save(folder_route)
        else:
            get_data["image"] = ''
        data_handler.add_new_question(get_data)
        question_id = data_handler.get_question_by_sub_time()[0]['max']
        return redirect(url_for("display_question", question_id=question_id))

    return render_template('question.html')


@app.route("/question/<question_id>/edit", methods=["GET", "POST"])
def edit_question(question_id):
    questions = data_handler.get_all_questions()
    if request.method == 'POST':

        edited_question = request.form.to_dict()
        data_handler.edit_question(question_id, edited_question)
        return redirect(url_for("display_question", question_id=question_id))

    target_question = data_handler.get_question_by_id(question_id)
    return render_template("question.html", question=target_question)


@app.route("/answer/<answer_id>/edit", methods=["GET", "POST"])
def edit_answer(answer_id):
    if request.method == 'POST':
        edited_answer = request.form.to_dict()
        data_handler.edit_answer(answer_id, edited_answer)
        return redirect(url_for("display_question", answer_id=answer_id))

    target_answer = data_handler.get_answer_by_id(answer_id)
    return render_template("add_new_answer.html", answer=target_answer)


@app.route("/question/<question_id>/delete")
def delete_question(question_id):

    data_handler.delete_question_by_id_sql(question_id)

    return redirect("/list")


@app.route("/answer/<answer_id>/delete")
def delete_answer(answer_id):

    target_answer = data_handler.get_answer_by_id(answer_id)
    question_id = target_answer["question_id"]
    data_handler.delete_answer_by_id_sql(answer_id)

    return redirect(f'/question/{question_id}')


@app.route("/question/<question_id>/vote_up")
def question_vote_up(question_id):
    data_handler.increment_vote_number('question', question_id, 1)
    return redirect("/list")


@app.route("/question/<question_id>/vote_down")
def question_vote_down(question_id):
    data_handler.increment_vote_number('question', question_id, -1)
    return redirect("/list")


@app.route("/question/<question_id>/new_answer", methods=["GET", "POST"])
def add_new_answer(question_id):
    if request.method == "POST":
        get_data = request.form.to_dict()
        if secure_filename(request.files['image'].filename) != "":
            get_data["image"] = secure_filename(request.files['image'].filename)
            folder_route = UPLOAD_FOLDER_ANSWERS + get_data["image"]
            request.files["image"].save(folder_route)
        else:
            get_data["image"] = ''
        get_data["question_id"] = question_id
        data_handler.add_new_answer(get_data)

        return redirect(url_for("display_question", question_id=question_id))
    return render_template('add_new_answer.html', question_id=question_id)


@app.route("/answer/<answer_id>/new-comment", methods=["POST"])
def add_comment_to_answer(answer_id):

    if request.method == "POST":
        new_comment = request.form.to_dict()
        data_handler.add_new_comment(new_comment)
        question_id = data_handler.get_question_id_by_answer_id(answer_id)

        return redirect(url_for("display_question", question_id=question_id))

    return render_template("add_new_comment.html")


@app.route("/question/<question_id>/new-comment", methods=["GET", "POST"])
def add_new_comment_to_question(question_id):
    if request.method == "POST":
        new_comment = {'question_id': question_id,
                       'answer_id': None,
                       'message': request.form.get("new-comment"),
                       'edited_count': 0}
        data_handler.add_new_comment_to_question(new_comment)
        return redirect(url_for("display_question", question_id=question_id))

    return render_template('add_new_comment.html', question_id=question_id)


@app.route("/answer/<answer_id>/vote_up")
def answer_vote_up(answer_id):
    data_handler.increment_vote_number('answer', answer_id, 1)
    question_id = data_handler.get_question_id_by_answer_id(answer_id)
    question_id = question_id["question_id"]

    return redirect(f'/question/{question_id}')


@app.route("/answer/<answer_id>/vote_down")
def answer_vote_down(answer_id):
    data_handler.increment_vote_number('answer', answer_id, -1)
    question_id = data_handler.get_question_id_by_answer_id(answer_id)
    question_id = question_id["question_id"]

    return redirect(f'/question/{question_id}')


@app.route("/search")
def search_page():

    search_phrase = request.args.get('q')

    if search_phrase:
        found_questions = data_handler.search_table('question', search_phrase)
        found_answers = data_handler.search_table('answer', search_phrase)
        if len(found_questions) != 0:
            found_questions = data_handler.highlight_search_phrase(found_questions, search_phrase)
        if len(found_answers) != 0:
            found_answers = data_handler.highlight_search_phrase(found_answers, search_phrase)

        return render_template('results.html', questions=found_questions, answers=found_answers)
    return redirect('/list')


if __name__ == "__main__":
    app.run(
        debug=True,
    )
