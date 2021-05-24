from flask import Flask, render_template, request, redirect

import data_handler


app = Flask(__name__)


@app.route("/")
@app.route("/list")
def list_page():
    questions = data_handler.sort_questions(True)
    return render_template(list.html, header=data_handler.QUESTIONS_HEADER, questions=questions)


if __name__ == "__main__":
    app.run(
        debug=True,
    )
