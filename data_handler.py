import connection
import time

QUESTIONS_HEADER = ['Id', 'Submission Time', 'View Number', 'Vote Number', 'Title', 'Message', 'Image']
ANSWERS_HEADER = ['Id', 'Submission Time', 'Vote Number', 'Question Id', 'Message', 'Image']


def sort_questions(order_by, order_direction):
    sorting = True if order_direction == 'desc' else False
    read_csvfile = connection.open_csvfile(connection.DATA_FILE_PATH_QUESTIONS)
    sorted_listofdict = sorted(read_csvfile, key=lambda x: x[order_by], reverse=sorting)
    return sorted_listofdict


def delete_question_by_id(question_id):
    questions = connection.open_csvfile(connection.DATA_FILE_PATH_QUESTIONS)
    for question in questions:
        if question_id == question["id"]:
            questions.remove(question)

    connection.write_files(connection.DATA_FILE_PATH_QUESTIONS, connection.QUESTION_KEYS, questions)

    # still need to write back to the file

def find_question(questions, question_id):
    for question in questions:
        if question["id"] == question_id:
            target_question = question
            return target_question
    return None

def edit_question(questions, edited_question, question_id):
    edited_question["submission_time"] = time.time()
    for question_index in range(len(questions)):
        if questions[question_index]["id"] == question_id:
            questions[question_index] = edited_question
            write_files(connection.DATA_FILE_PATH_QUESTIONS, connection.QUESTION_KEYS, questions)
    return None

# writing back to csv according to id(ascending)? + use QUESTION_KEYS/ANSWER_KEYS to make order within rows