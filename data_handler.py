import os.path

import asd
import connection
from datetime import datetime


QUESTIONS_HEADER = ['Id', 'Submission Time', 'View Number', 'Vote Number', 'Title', 'Message', 'Image']
ANSWERS_HEADER = ['Id', 'Submission Time', 'Vote Number', 'Question Id', 'Message', 'Image']
DATA_FILE_PATH_QUESTIONS = 'sample_data/question.csv'
DATA_FILE_PATH_ANSWERS = 'sample_data/answer.csv'
QUESTION_KEYS = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWER_KEYS = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


def sort_data(filepath, order_by, order_direction):
    sorting = True if order_direction == 'desc' else False
    read_csvfile = asd.open_csvfile(filepath)
    sorted_listofdict = sorted(read_csvfile, key=lambda x: (0, int(x[order_by])) if (x[order_by].isdigit() or x[order_by][0] == "-") else (1, x[order_by]), reverse=sorting)
    return sorted_listofdict


@connection.connection_handler
def get_last_five_questions_by_time(cursor):
    cursor.execute("""
                    SELECT * FROM question
                    ORDER BY submission_time DESC
                    LIMIT 5;
                    """)
    return cursor.fetchall()


@connection.connection_handler
def get_all_data(cursor, table, order_by, direction):
    cursor.execute(f"""
                    SELECT * FROM {table}
                    ORDER BY {order_by} {direction}
                    """)

    return cursor.fetchall()


@connection.connection_handler
def add_new_question(cursor, question):
    timestamp = generate_timestamp()
    cursor.execute("""
                     INSERT INTO question (submission_time, view_number, vote_number, title, message, image)
                     VALUES (%(timestamp)s, 0, 0, %(title)s, %(message)s, %(image)s) RETURNING id;
                     """, {'timestamp': timestamp, 'title': question['title'], 'message': question['message'],
                           'image': question['image']})
    return cursor.fetchone()


@connection.connection_handler
def add_new_answer(cursor, answer):
    timestamp = generate_timestamp()
    cursor.execute("""
                     INSERT INTO answer (submission_time, vote_number, question_id, message, image)
                     VALUES (%(timestamp)s, 0, %(question_id)s, %(message)s, %(image)s);
                     """,
                   {'timestamp': timestamp, 'question_id': answer['question_id'], 'message': answer['message'],
                    'image': answer['image']})


@connection.connection_handler
def get_all_questions(cursor):
    cursor.execute("""
                    SELECT * FROM question
                    """)
    return cursor.fetchall()


@connection.connection_handler
def get_question_by_id(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM question
                    WHERE id = %(id)s
                    """,
                   {'id': question_id})
    return cursor.fetchone()


@connection.connection_handler
def get_answer_by_id(cursor, answer_id):
    cursor.execute("""
                    SELECT * FROM answer
                    WHERE id = %(id)s
                    """,
                   {'id': answer_id})
    return cursor.fetchall()


@connection.connection_handler
def get_answer_by_id(cursor, answer_id):
    cursor.execute("""
                    SELECT * FROM answer
                    WHERE id = %(id)s
                    """,
                   {'id': answer_id})
    return cursor.fetchall()


@connection.connection_handler
def get_comment_by_id(cursor, comment_id):
    cursor.execute(f"""
                    SELECT * FROM comment
                    WHERE id = %(id)s
                    """,
                   {'id': comment_id})
    return cursor.fetchone()


@connection.connection_handler
def edit_comment(cursor, comment_id, edited):
    timestamp = generate_timestamp()
    cursor.execute("""
                    UPDATE comment
                    SET message = %(message)s,
                        submission_time = %(timestamp)s, edited_count = edited_count + 1
                    WHERE id = %(id)s
                    """,
                   {'message': edited['message'], 'timestamp': timestamp, 'id': comment_id})


@connection.connection_handler
def edit_question(cursor, question_id, edited):
    cursor.execute(f"""
                    UPDATE question
                    SET title = {edited['title']}, message = {edited['message']}
                    WHERE id = {question_id}
                   """)


@connection.connection_handler
def edit_answer(cursor, answer_id, edited):
    cursor.execute(f"""
                    UPDATE answer
                    SET message = {edited['message']}, image = {edited['image']}
                    WHERE id = {answer_id}
                   """)


@connection.connection_handler
def delete_question_by_id_sql(cursor, question_id):
    cursor.execute("""
                    DELETE from question
                    WHERE id = %(id)s
                   """,
                   {'id': question_id})


@connection.connection_handler
def delete_answer_by_id_sql(cursor, answer_id):
    cursor.execute("""
                    DELETE from answer
                    WHERE id = %(id)s
                   """,
                   {'id': answer_id})


@connection.connection_handler
def increment_view_number(cursor, question_id):
    cursor.execute("""
                   UPDATE question
                   SET view_number = (SELECT view_number FROM question
                                      WHERE id = %(question_id)s) + 1
                   WHERE id=%(question_id)s
                   """, {'question_id': question_id})


@connection.connection_handler
def increment_vote_number(cursor, table, specific_id, increment):  # table: question, answer; increment: 1, -1
    cursor.execute(f"""
                   UPDATE {table}
                   SET vote_number = vote_number + {increment}
                   WHERE id = {specific_id}
                   """)


@connection.connection_handler
def get_question_id_by_answer_id(cursor, answer_id):
    cursor.execute("""
                    SELECT question_id FROM answer
                    WHERE id = %(answer_id)s
                    """,
                   {'answer_id': answer_id})
    return cursor.fetchall()


@connection.connection_handler
def search_table(cursor, phrase, order='submission_time'):
    cursor.execute(f"""
                    SELECT question.id AS q_id,
                    question.submission_time AS q_submission_time,
                    view_number,
                    question.vote_number AS q_vote_number,
                    title,
                    question.message AS q_message,
                    question.image AS q_image,
                    answer.id AS a_id,
                    answer.submission_time AS a_submission_time,
                    answer.vote_number AS a_vote_number,
                    question_id,
                    answer.message AS a_message,
                    answer.image AS a_image
                    FROM question FULL OUTER JOIN answer ON question.id = answer.question_id
                    WHERE 
                        title LIKE '%{phrase}%'
                        OR question.message LIKE '%{phrase}%'
                        OR answer.message LIKE '%{phrase}%'
                    ORDER BY question.{order}
                    """)
    return cursor.fetchall()


def highlight_search_phrase(datatable, phrase):
    for entry_index in range(len(datatable)):
        datatable[entry_index]['title'] = datatable[entry_index]['title'].replace(phrase, f'<mark>{phrase}</mark>')
        datatable[entry_index]['q_message'] = datatable[entry_index]['q_message'].replace(phrase, f'<mark>{phrase}</mark>')
        if datatable[entry_index]['a_message'] is not None:
            datatable[entry_index]['a_message'] = datatable[entry_index]['a_message'].replace(phrase, f'<mark>{phrase}</mark>')
    return datatable


@connection.connection_handler
def add_new_comment(cursor, comment):
    timestamp = generate_timestamp()
    cursor.execute(f"""
                    INSERT INTO comment (question_id, answer_id, message, submission_time, edited_count)
                    VALUES ({comment['question_id']}, {comment['answer_id']},
                            {comment['message']}, {timestamp}, {0}
                    """)


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


@connection.connection_handler
def add_new_comment_to_question(cursor, comment_dict):
    timestamp = generate_timestamp()
    cursor.execute("""
                        INSERT INTO comment(question_id, answer_id, message, submission_time, edited_count)
                        VALUES(%(question_id)s, %(answer_id)s, %(message)s, %(submission_time)s, %(edited_count)s);
                        """,
                       {'question_id': comment_dict['question_id'],
                        'answer_id': comment_dict['answer_id'],
                        'message': comment_dict['message'],
                        'submission_time': timestamp,
                        'edited_count': comment_dict['edited_count']})


@connection.connection_handler
def get_all_tag(cursor):
    cursor.execute("""
                    SELECT * FROM tag
                    """)
    return cursor.fetchall()


@connection.connection_handler
def add_new_tag(cursor, tag_name):
    cursor.execute("""
                        INSERT INTO tag (name)
                        VALUES(%(tag_name)s)
                        """, {'tag_name':tag_name})


@connection.connection_handler
def delete_tag_by_question_id(cursor, question_id, tag_id):
    cursor.execute("""
                    DELETE from question_tag
                    WHERE question_id = %(question_id)s AND tag_id = %(tag_id)s
                    """,
                   {'question_id': question_id, 'tag_id':tag_id})


@connection.connection_handler
def get_tag_id_by_name(cursor, tag_name):
    cursor.execute("""
                    SELECT id FROM tag
                    WHERE name = %(tag_name)s
                   """,
                   {'tag_name': tag_name})
    return cursor.fetchone()


@connection.connection_handler
def get_tag_by_name(cursor, tag_name):
    cursor.execute("""
                    SELECT name FROM tag
                    WHERE name = %(tag_name)s
                   """,
                   {'tag_name': tag_name})
    return cursor.fetchall()


@connection.connection_handler
def get_tags_id_by_question_id(cursor, id):
    cursor.execute("""
                    SELECT tag_id FROM question_tag
                    WHERE question_id = %(id)s
                   """,
                   {'id': id})
    return cursor.fetchone()


@connection.connection_handler
def get_tags_by_tag_id(cursor, tag_id):
    cursor.execute("""
                    SELECT * FROM tag
                    WHERE id = %(tag_id)s
                   """,
                   {'tag_id': tag_id})
    return cursor.fetchone()


@connection.connection_handler
def add_tag_id_to_question_tag(cursor, question_id, tag_id):
    cursor.execute("""
                        INSERT INTO question_tag(question_id, tag_id)
                        VALUES(%(question_id)s, %(tag_id)s)
                        """, {'question_id':question_id, 'tag_id':tag_id})


@connection.connection_handler
def get_tags_by_question_id(cursor, question_id):
    cursor.execute("""
                    SELECT name FROM tag
                    WHERE id = (SELECT tag_id FROM question_tag
                       WHERE question_id = %(question_id)s)
                        """, {'question_id':question_id})
    return cursor.fetchall()

