import os.path

import asd
import conection
from datetime import datetime


QUESTIONS_HEADER = ['Id', 'Submission Time', 'View Number', 'Vote Number', 'Title', 'Message', 'Image']
ANSWERS_HEADER = ['Id', 'Submission Time', 'Vote Number', 'Question Id', 'Message', 'Image']




def sort_data(filepath, order_by, order_direction):
    sorting = True if order_direction == 'desc' else False
    read_csvfile = asd.open_csvfile(filepath)
    sorted_listofdict = sorted(read_csvfile, key=lambda x: (0, int(x[order_by])) if (x[order_by].isdigit() or x[order_by][0] == "-") else (1, x[order_by]), reverse=sorting)
    return sorted_listofdict


@conection.connection_handler
def get_last_five_questions_by_time(cursor):
    cursor.execute("""
                    SELECT * FROM question
                    ORDER BY submission_time DESC
                    LIMIT 5;
                    """)
    return cursor.fetchall()


@conection.connection_handler
def get_all_data(cursor, table, order_by, direction):
    cursor.execute(f"""
                    SELECT * FROM {table}
                    ORDER BY {order_by} {direction}
                    """)

    return cursor.fetchall()


@conection.connection_handler
def add_new_question(cursor, question):
    timestamp = generate_timestamp()
    cursor.execute("""
                     INSERT INTO question (submission_time, view_number, vote_number, title, message, image
                     VALUES (%(timestamp)s, 0, 0, %(title)s, %(message)s, %(image)s
                     """, {'timestamp': timestamp, 'title': question['title'], 'message': question['message'],
                           'image': question['image']})


@conection.connection_handler
def add_new_answer(cursor, answer):
    timestamp = generate_timestamp()
    cursor.execute("""
                     INSERT INTO answer (submission_time, vote_number, question_id, message, image
                     VALUES (%(timestamp)s, 0, %(question_id)s, %(title)s, %(message)s, %(image)s
                     """, {'timestamp': timestamp, 'question_id': answer['question_id'], 'message': answer['message'],
                           'image': answer['image']})


@conection.connection_handler
def get_all_questions(cursor):
    cursor.execute("""
                    SELECT * FROM questions
                    """)
    return cursor.fetchall()


@conection.connection_handler
def get_question_by_id(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM questions
                    WHERE id = %(id)s
                    """,
                   {'id': question_id})
    return cursor.fetchall()


@conection.connection_handler
def get_answer_by_id(cursor, answer_id):
    cursor.execute("""
                    SELECT * FROM answer
                    WHERE id = %(id)s
                    """,
                   {'id': answer_id})
    return cursor.fetchall()


@conection.connection_handler
def edit_question(cursor, question_id, edited):
    cursor.execute(f"""
                    UPDATE question
                    SET title = {edited['title']}, message = {edited['message']}
                    WHERE id = {question_id}
                   """)


@conection.connection_handler
def delete_question_by_id_sql(cursor, question_id):
    cursor.execute("""
                    DELETE from question
                    WHERE id = %(id)s
                   """,
                   {'id': question_id})


@conection.connection_handler
def delete_answer_by_id_sql(cursor, answer_id):
    cursor.execute("""
                    DELETE from answer
                    WHERE id = %(id)s
                   """,
                   {'id': answer_id})


@conection.connection_handler
def increment_view_number(cursor, question_id):
    cursor.execute("""
                   UPDATE question
                   SET view_number = (SELECT view_number FROM question
                                      WHERE id = %(question_id)s) + 1
                   WHERE id=%(question_id)s
                   """, {'question_id': question_id})


def delete_answer_by_id(answer_id):
    answers = asd.open_csvfile(asd.DATA_FILE_PATH_ANSWERS)
    for answer in answers:
        if answer_id == answer["id"]:
            answers.remove(answer)
    
    asd.write_files(asd.DATA_FILE_PATH_ANSWERS, asd.ANSWER_KEYS, answers)


def delete_question_by_id(question_id):
    questions = asd.open_csvfile(asd.DATA_FILE_PATH_QUESTIONS)
    for question in questions:
        if question_id == question["id"]:
            questions.remove(question)

    asd.write_files(asd.DATA_FILE_PATH_QUESTIONS, asd.QUESTION_KEYS, questions)





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
                asd.write_files(asd.DATA_FILE_PATH_ANSWERS, asd.ANSWER_KEYS, database)
            else:
                asd.write_files(asd.DATA_FILE_PATH_QUESTIONS, asd.QUESTION_KEYS, database)
    return None




