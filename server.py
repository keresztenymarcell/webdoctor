from flask import Flask, render_template, request, session, redirect, flash, url_for
import data_handler
import os


DIRNAME = os.path.dirname(__file__)
UPLOAD_FOLDER_QUESTIONS = DIRNAME + "/static/pictures/question_pictures/"
UPLOAD_FOLDER_ANSWERS = DIRNAME + "/static/pictures/answer_pictures/"


app = Flask(__name__)

app.secret_key = b'_akJFh3sjfjbhsdjb/'


@app.route("/")
def main_page():
    question_data = data_handler.get_last_five_questions_by_time()
    return render_template("index.html", questions=question_data)


@app.route("/users")
def list_users():
    user_details = data_handler.get_all_data('users', 'reputation', 'desc')
    return render_template("users.html", user_details=user_details)


@app.route("/user/<user_id>")
def profile_page(user_id):
    details = data_handler.get_data_by_id('users', user_id)
    print(details)
    return render_template("profile.html", details=details)


@app.route("/list")
def list_page():
    order_by = request.args.get('order_by', 'submission_time')
    order_direction = request.args.get('order_direction', 'desc')
    questions = data_handler.get_all_data('question', order_by, order_direction)
    comments = data_handler.get_all_data('comment', 'submission_time', 'desc')
    return render_template('list.html', header=data_handler.QUESTIONS_HEADER, keys=data_handler.QUESTION_KEYS,
                           questions=questions, orderby=order_by, orderdir=order_direction, comments=comments)


@app.route("/question/<question_id>")
def display_question(question_id):
    question = data_handler.get_data_by_id("question", question_id)
    answers = data_handler.get_all_data("answer", "vote_number", "desc")
    data_handler.increment_view_number(question_id)
    tags = data_handler.get_tags_by_question_id(question_id)
    comments = data_handler.get_all_data('comment', 'submission_time', 'desc')
    return render_template('display_question.html', question=question, answers=answers, tags=tags, comments=comments)


@app.route("/add-question", methods=["GET", "POST"])
def write_questions():
    do_edit = False
    if request.method == "POST":
        get_data = request.form.to_dict()
        get_data['user_id'] = session['user_id']
        data_handler.image_data_handling(UPLOAD_FOLDER_QUESTIONS, request.files['image'], get_data, do_edit)
        question_id = data_handler.add_new_question(get_data)['id']
        data_handler.update_user('questions_count', get_data['user_id'])

        return redirect(url_for("display_question", question_id=question_id))
    return render_template('question.html')


@app.route("/question/<question_id>/new_answer", methods=["GET", "POST"])
def add_new_answer(question_id):
    do_edit = False
    if request.method == "POST":
        get_data = request.form.to_dict()
        data_handler.image_data_handling(UPLOAD_FOLDER_ANSWERS, request.files['image'], get_data, do_edit)
        get_data["question_id"] = question_id
        get_data['user_id'] = session['user_id']
        data_handler.add_new_answer(get_data)
        data_handler.update_user('answers_count', get_data['user_id'])
        return redirect(url_for("display_question", question_id=question_id))

    return render_template('add_new_answer.html', question_id=question_id)


@app.route("/question/<question_id>/edit", methods=["GET", "POST"])
def edit_question(question_id):
    do_edit = True
    if request.method == 'POST':
        edited_question = request.form.to_dict()
        data_handler.image_data_handling(UPLOAD_FOLDER_QUESTIONS, request.files['image'], edited_question, do_edit)
        data_handler.edit_question(edited_question)
        return redirect(url_for("display_question", question_id=question_id))

    target_question = data_handler.get_data_by_id('question', question_id)
    return render_template("question.html", question=target_question)


@app.route("/answer/<answer_id>/edit", methods=["GET", "POST"])
def edit_answer(answer_id):
    do_edit = True
    if request.method == 'POST':
        edited_answer = request.form.to_dict()
        data_handler.image_data_handling(UPLOAD_FOLDER_ANSWERS, request.files['image'], edited_answer, do_edit)
        data_handler.edit_answer(edited_answer)
        question_id = edited_answer['question_id']
        return redirect(url_for("display_question", question_id=question_id))

    target_answer = data_handler.get_data_by_id('answer', answer_id)
    return render_template("add_new_answer.html", answer=target_answer)


@app.route("/question/<question_id>/delete")
def delete_question(question_id):
    image_name = data_handler.get_image_name_by_id('question', question_id)['image']
    image_list = os.listdir(UPLOAD_FOLDER_QUESTIONS)
    if image_name in image_list:
        file_path = UPLOAD_FOLDER_QUESTIONS + image_name
        os.remove(file_path)
    data_handler.delete_data_by_id('question', question_id)

    return redirect("/list")


@app.route("/answer/<answer_id>/delete")
def delete_answer(answer_id):
    target_answer = data_handler.get_data_by_id('answer', answer_id)
    question_id = target_answer["question_id"]

    image_name = data_handler.get_image_name_by_id('answer', answer_id)['image']
    image_list = os.listdir(UPLOAD_FOLDER_ANSWERS)
    if image_name in image_list:
        file_path = UPLOAD_FOLDER_ANSWERS + image_name
        os.remove(file_path)
        data_handler.delete_data_by_id('answer', answer_id)

    return redirect(f'/question/{question_id}')


@app.route("/question/<question_id>/vote_up")
def question_vote_up(question_id):
    data_handler.increment_vote_number('question', question_id, 1)
    data_handler.reputation_manager("question", question_id, 5)
    return redirect("/list")


@app.route("/question/<question_id>/vote_down")
def question_vote_down(question_id):
    data_handler.increment_vote_number('question', question_id, -1)
    data_handler.reputation_manager('question', question_id, -2)
    return redirect("/list")


@app.route("/answer/<answer_id>/vote_up")
def answer_vote_up(answer_id):
    data_handler.increment_vote_number('answer', answer_id, 1)
    data_handler.reputation_manager('answer', answer_id, 10)
    question_id = data_handler.get_question_id_by_answer_id(answer_id)
    question_id = question_id["question_id"]
    return redirect(f'/question/{question_id}')


@app.route("/answer/<answer_id>/vote_down")
def answer_vote_down(answer_id):
    data_handler.increment_vote_number('answer', answer_id, -1)
    data_handler.reputation_manager('answer', answer_id, -2)
    question_id = data_handler.get_question_id_by_answer_id(answer_id)
    question_id = question_id["question_id"]
    return redirect(f'/question/{question_id}')


@app.route("/answer/<answer_id>/new-comment", methods=["GET", "POST"])
def add_comment_to_answer(answer_id):
    question_id = data_handler.get_question_id_by_answer_id(answer_id)['question_id']
    if request.method == "POST":
        new_comment = {'question_id': None,
                       'answer_id': answer_id,
                       'message': request.form.get("new-comment2"),
                       'edited_count': 0,
                       'user_id': session['user_id']}
        data_handler.add_new_comment(new_comment)
        return redirect(url_for("display_question", question_id=question_id))

    return render_template("add_new_comment.html", answer_id=answer_id)


@app.route("/question/<question_id>/new-comment", methods=["GET", "POST"])
def add_new_comment_to_question(question_id):
    if request.method == "POST":
        new_comment = {'question_id': question_id,
                       'answer_id': None,
                       'message': request.form.get("new-comment"),
                       'edited_count': 0,
                       'user_id': session['user_id']}
        data_handler.add_new_comment(new_comment)
        data_handler.update_user('comments_count', session['user_id'])
        return redirect(url_for("display_question", question_id=question_id))

    return render_template("add_new_comment.html", question_id=question_id)


@app.route("/comment/<comment_id>/edit", methods=["GET", "POST"])
def edit_comment(comment_id):
    comment = data_handler.get_data_by_id('comment', comment_id)
    question_id = comment["question_id"]

    if request.method == "POST":
        if comment['question_id']:
            edited_comment = request.form.to_dict()
            data_handler.edit_comment(comment_id, edited_comment)

            return redirect(url_for("display_question", question_id=question_id))
        else:
            edited_comment = request.form.to_dict()
            answer_id = comment['answer_id']
            question_id = data_handler.get_question_id_by_answer_id(answer_id)['question_id']
            data_handler.edit_comment(comment_id, edited_comment)

            return redirect(url_for("display_question", question_id=question_id))

    return render_template("edit_comment.html", comment=comment)


@app.route("/comment/<comment_id>/delete")
def delete_comment(comment_id):
    comment = data_handler.get_data_by_id('comment', comment_id)
    if comment["question_id"]:
        question_id = comment['question_id']
        data_handler.delete_data_by_id('comment', comment_id)
        return redirect(url_for("display_question", question_id=question_id))
    else:
        answer_id = comment['answer_id']
        question_id = data_handler.get_question_id_by_answer_id(answer_id)['question_id']
        data_handler.delete_data_by_id('comment', comment_id)
        return redirect(url_for("display_question", question_id=question_id))


@app.route("/search")
def search_page():
    search_phrase = request.args.get('q')
    tag_type = 'mark'

    if search_phrase:
        result = data_handler.search_table(search_phrase)
        if len(result) != 0:
            result = data_handler.highlight_search_phrase(result, search_phrase, tag_type)

        return render_template('results.html', results=result, phrase=search_phrase, tag_type=tag_type)
    return redirect('/list')


@app.route("/question/<question_id>/new-tag", methods=["GET", "POST"])
def add_tag(question_id):
    new_tag = request.form.get("new-tag")
    exist_tag = request.form.get("existing-tag")
    if request.method == "POST":
        if new_tag:
            tag_id = data_handler.add_new_tag(new_tag)['id']
            data_handler.add_tag_id_to_question_tag(tag_id, question_id)
            return redirect(url_for("display_question", question_id=question_id))
        else:
            tag_id = data_handler.get_tag_id_by_name(exist_tag)['id']
            data_handler.add_tag_id_to_question_tag(tag_id, question_id)
            tags = data_handler.get_tags_by_question_id(question_id)
            return redirect(url_for("display_question", question_id=question_id, tags=tags))

    filtered_tags = data_handler.filter_tags(question_id)
    return render_template('add_new_tag.html', question_id=question_id, tags=filtered_tags)


@app.route("/question/<question_id>/tag/<tag_id>/delete", methods=["GET", "POST"])
def remove_tag(question_id, tag_id):
    data_handler.delete_tag_by_question_id(question_id, tag_id)
    return redirect(url_for("display_question", question_id=question_id))


@app.route("/registration", methods=["GET", "POST"])
def registration_page():
    if request.method == "POST":
        user_email = request.form['email']
        user_password = request.form['psw']
        user_name = request.form['user_name']
        is_new_user = data_handler.check_if_new_user(user_email)
        if is_new_user:
            data_handler.register_user(user_email, user_password, user_name)
            return redirect("/login")
        flash ("This e-mail has already been used")
        return render_template("registration.html")
    return render_template("registration.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_info = request.form.to_dict()      # email, psw
        is_new_user = data_handler.check_if_new_user(user_info['email'])
        if is_new_user:
            return redirect(url_for('registration_page'))
        hashed_user_password = data_handler.get_user_password(user_info)['password']
        if data_handler.verify_password(user_info['psw'], hashed_user_password):
            session['mail'] = user_info['email']
            user_id = data_handler.get_user_id_by_mail(user_info['email'])['id']
            user_data = data_handler.get_data_by_id('users', user_id)
            session['username'] = user_data['user_name']
            session['logged_in'] = True
            session['user_id'] = user_id
            questions = data_handler.get_last_five_questions_by_time()
            return render_template('index.html', questions=questions)
        flash("Invalid login attempt")
        return render_template('login.html')
    return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('user_name', None)
    session.pop('logged_in', None)
    return redirect(url_for('main_page'))


@app.route("/question/<question_id>/remove_accept/<answer_id>")
def remove_accept(question_id,answer_id):
    data_handler.remove_accept_status(answer_id)
    data_handler.reputation_manager('answer', answer_id, -15)
    return redirect(url_for('display_question', question_id=question_id))


@app.route('/question/<question_id>/accept_answer/<answer_id>')
def accept_answer(question_id, answer_id):
    data_handler.accept_answer(answer_id)
    data_handler.reputation_manager('answer', answer_id, 15)
    return redirect(url_for('display_question', question_id=question_id))


@app.route('/tags')
def tag_page():
    all_tags = data_handler.get_marked_questions()
    return render_template('tag.html', tags=all_tags)



if __name__ == "__main__":
    app.run(
        debug=True,
    )
