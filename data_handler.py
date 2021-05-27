import os.path

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


def delete_answer_by_id(answer_id):
    answers = connection.open_csvfile(connection.DATA_FILE_PATH_QUESTIONS)
    for answer in answers:
        if answer_id == answer["id"]:
            answers.remove(answer)
    
    connection.write_files(connection.open_csvfile(connection.DATA_FILE_PATH_ANSWERS, connection.ANSWERS_KEYS, answers))


def generate_id(database):
    if database is []:
        new_id = 0
    else:
        new_id = int(database[-1]["id"]) + 1

    return new_id


def find_question(questions, question_id):
    for question in questions:
        if question["id"] == question_id:
            return question
    return None


def find_answer(answers, question_id, answer_id):
    for answer in answers:
        if answer["question_id"] == question_id:
            if answer["id"] == answer_id:
                return answer
    return None


def edit_database(database, edited_data, data_id):
    edited_data["submission_time"] = time.time()
    for data_index in range(len(database)):
        if database[data_index]["id"] == data_id:
            database[data_index] = edited_data
            if "question_id" in database[0].keys():
                connection.write_files(connection.DATA_FILE_PATH_ANSWERS, connection.ANSWER_KEYS, database)
            else:
                connection.write_files(connection.DATA_FILE_PATH_QUESTIONS, connection.QUESTION_KEYS, database)
    return None

# writing back to csv according to id(ascending)? + use QUESTION_KEYS/ANSWER_KEYS to make order within rows
