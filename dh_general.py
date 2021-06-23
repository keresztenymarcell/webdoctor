import re
import connection, bcrypt
from werkzeug.utils import secure_filename
from datetime import datetime

import dh_tags


@connection.connection_handler
def search_question_table(cursor, phrase, order='submission_time'):
    cursor.execute(f"""
                    SELECT * FROM question
                    WHERE 
                        title ILIKE '%{phrase}%'
                        OR message ILIKE '%{phrase}%'
                    ORDER BY {order}
    """)
    return cursor.fetchall()


@connection.connection_handler
def search_answer_table(cursor, phrase, order='submission_time'):
    cursor.execute(f"""
                    SELECT * FROM answer
                    WHERE 
                        message ILIKE '%{phrase}%'
                    ORDER BY {order}
    """)
    return cursor.fetchall()


@connection.connection_handler
def get_image_name_by_id(cursor, table, id):
    cursor.execute(f"""
                    SELECT image FROM {table}
                    WHERE id = {id}

                    """)
    return cursor.fetchone()


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


