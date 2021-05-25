from flask import Flask, render_template, request, redirect, url_for

import data_handler, connection

ANSWER_KEYS = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
app = Flask(__name__)


@app.route("/")
@app.route("/list", defaults={'sort_parameters': 'order_by=submission_time&order_direction=desc'})
@app.route("/list/<sort_parameters>")
def list_page(sort_parameters):
    order_by = sort_parameters.split("&")[0].split("=")[1]
    order_direction = sort_parameters.split("&")[1].split("=")[1]
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
        questions.append(get_data)
        connection.write_files(connection.DATA_FILE_PATH_QUESTIONS,connection.QUESTION_KEYS,questions)
        return redirect(url_for("display_question", question_id=question_id))

    return render_template('question.html')
    




@app.route("/question/<question_id>/delete")
def delete_question(question_id):
    data_handler.delete_question_by_id(question_id)
    return redirect(url_for("display_question", question_id=question_id))


@app.route("/answer/<answer_id>/delete")
def delete_answer(answer_id):
    data_handler.delete_answer_by_id(question_id)
    return









if __name__ == "__main__":
    app.run(
        debug=True,
    )
