import os.path

import connection
import database_common
from datetime import datetime


QUESTIONS_HEADER = ['Id', 'Submission Time', 'View Number', 'Vote Number', 'Title', 'Message', 'Image']
ANSWERS_HEADER = ['Id', 'Submission Time', 'Vote Number', 'Question Id', 'Message', 'Image']


def sort_data(filepath, order_by, order_direction):
    sorting = True if order_direction == 'desc' else False
    read_csvfile = connection.open_csvfile(filepath)
    sorted_listofdict = sorted(read_csvfile, key=lambda x: (0, int(x[order_by])) if (x[order_by].isdigit() or x[order_by][0] == "-") else (1, x[order_by]), reverse=sorting)
    return sorted_listofdict


@database_common.connection_handler
def add_new_question(cursor, question):
    timestamp = generate_timestamp()
    cursor.execute("""
                     INSERT INTO question (submission_time, view_number, vote_number, title, message, image
                     VALUES (%(timestamp)s, 0, 0, %(title)s, %(message)s, %(image)s
                     """, {'timestamp': timestamp, 'title': question['title'], 'message': question['message'],
                           'image': question['image']})


@database_common.connection_handler
def add_new_question(cursor, answer):
    timestamp = generate_timestamp()
    cursor.execute("""
                     INSERT INTO answer (submission_time, vote_number, question_id, message, image
                     VALUES (%(timestamp)s, 0, %(question_id)s, %(title)s, %(message)s, %(image)s
                     """, {'timestamp': timestamp, 'question_id': answer['question_id'], 'message': answer['message'],
                           'image': answer['image']})



def delete_question_by_id(question_id):
    questions = connection.open_csvfile(connection.DATA_FILE_PATH_QUESTIONS)
    for question in questions:
        if question_id == question["id"]:
            questions.remove(question)

    connection.write_files(connection.DATA_FILE_PATH_QUESTIONS, connection.QUESTION_KEYS, questions)

@database_common.connection_handler
def get_all_questions(cursor):
    cursor.execute("""
                    SELECT * FROM questions
                    """)
    return cursor.fetchall()


@database_common.connection_handler
def get_question_by_id(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM questions
                    WHERE id = %(id)s
                    """,
                   {'id': question_id})
    return cursor.fetchall()


@database_common.connection_handler
def get_question_by_id(cursor, answer_id):
    cursor.execute("""
                    SELECT * FROM questions
                    WHERE id = %(id)s
                    """,
                   {'id': answer_id})
    return cursor.fetchall()


@database_common.connection_handler
def delete_question_by_id_sql(cursor, question_id):
    cursor.execute("""
                    DELETE from question
                    WHERE id = %(id)s
                   """,
                   {'id': question_id})


def delete_answer_by_id(answer_id):
    answers = connection.open_csvfile(connection.DATA_FILE_PATH_ANSWERS)
    for answer in answers:
        if answer_id == answer["id"]:
            answers.remove(answer)
    
    connection.write_files(connection.DATA_FILE_PATH_ANSWERS, connection.ANSWER_KEYS, answers)


@database_common.connection_handler
def delete_answer_by_id_sql(cursor, answer_id):
    cursor.execute("""
                    DELETE from answer
                    WHERE id = %(id)s
                   """,
                   {'id': answer_id})


def generate_id(database):
    if database is []:
        new_id = 0
    else:
        new_id = int(database[-1]["id"]) + 1

    return new_id


def find_data(database, data_id):
    for data in database:
        if data["id"] == data_id:
            return data
    return None

def generate_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def edit_database(database, edited_data, data_id):
    for data_index in range(len(database)):
        if database[data_index]['id'] == data_id:
            database[data_index] = edited_data
            if "question_id" in database[0].keys():
                connection.write_files(connection.DATA_FILE_PATH_ANSWERS, connection.ANSWER_KEYS, database)
            else:
                connection.write_files(connection.DATA_FILE_PATH_QUESTIONS, connection.QUESTION_KEYS, database)
    return None




