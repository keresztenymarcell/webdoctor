import re
import connection, bcrypt
from werkzeug.utils import secure_filename
from datetime import datetime

import dh_tags


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
                        title ILIKE '%{phrase}%'
                        OR question.message ILIKE '%{phrase}%'
                        OR answer.message ILIKE '%{phrase}%'
                    ORDER BY question.{order}
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


