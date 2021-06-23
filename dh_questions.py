
import re
import connection, bcrypt
from werkzeug.utils import secure_filename
from datetime import datetime

import dh_general

QUESTIONS_HEADER = ['Id', 'Submission Time', 'View Number', 'Vote Number', 'Title', 'Message', 'Image']
QUESTION_KEYS = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']

@connection.connection_handler
def add_new_question(cursor, question):
    timestamp = dh_general.generate_timestamp()
    cursor.execute("""
                     INSERT INTO question (submission_time, view_number, vote_number, title, message, image, user_id)
                     VALUES (%(timestamp)s, 0, 0, %(title)s, %(message)s, %(image)s, %(user_id)s) RETURNING id;
                     """, {'timestamp': timestamp, 'title': question['title'], 'message': question['message'],
                           'image': question['image'], 'user_id':question['user_id']})
    return cursor.fetchone()
    

@connection.connection_handler
def edit_question(cursor, edited):
    cursor.execute("""
                    UPDATE question
                    SET title=%(title)s, message=%(message)s, image=%(image)s
                    WHERE id=%(question_id)s
                   """,
                   {'question_id': edited['id'],
                    'message': edited['message'],
                    'title': edited['title'],
                    'image': edited['image']}
                   )
                   

@connection.connection_handler
def get_question_id_by_answer_id(cursor, answer_id):
    cursor.execute("""
                    SELECT question_id FROM answer
                    WHERE id = %(answer_id)s
                    """,
                   {'answer_id': answer_id})
    return cursor.fetchone()



@connection.connection_handler
def get_marked_questions(cursor):
    cursor.execute("""
                    SELECT name AS Tagname,
                    COUNT(question_id) AS Marked_questions
                    FROM question_tag
                    Join tag t on question_tag.tag_id = t.id
                    GROUP BY name;
                    """)
    return cursor.fetchall()



@connection.connection_handler
def get_last_five_questions_by_time(cursor):
    cursor.execute("""
                    SELECT * FROM question
                    ORDER BY submission_time DESC
                    LIMIT 5;
                    """)
    return cursor.fetchall()










































