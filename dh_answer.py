
import connection, bcrypt
from werkzeug.utils import secure_filename
from datetime import datetime
import dh_general

ANSWERS_HEADER = ['Id', 'Submission Time', 'Vote Number', 'Question Id', 'Message', 'Image']
ANSWER_KEYS = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']



@connection.connection_handler
def add_new_answer(cursor, answer):
    timestamp = dh_general.generate_timestamp()
    cursor.execute("""
                     INSERT INTO answer (submission_time, vote_number, question_id, message, image, user_id)
                     VALUES (%(timestamp)s, 0, %(question_id)s, %(message)s, %(image)s, %(user_id)s);
                     """,
                   {'timestamp': timestamp, 'question_id': answer['question_id'], 'message': answer['message'],
                    'image': answer['image'], 'user_id': answer['user_id']})


@connection.connection_handler
def edit_answer(cursor, edited):
    cursor.execute("""
                    UPDATE answer
                    SET message=%(message)s, image=%(image)s
                    WHERE id=%(answer_id)s;
                   """,
                   {'answer_id': edited['id'],
                    'message': edited['message'],
                    'image': edited['image']}
                   )
                                     

@connection.connection_handler
def accept_answer(cursor, answer_id):
    query = """
            UPDATE answer
            SET accepted = TRUE
            WHERE id = %(answer_id)s
            """
    cursor.execute(query, {'answer_id': answer_id})


@connection.connection_handler
def remove_accept_status(cursor, answer_id):
    query = """
            UPDATE answer
            SET accepted = FALSE
            WHERE id = %(answer_id)s
            """
    cursor.execute(query, {"answer_id": answer_id})
    
    
@connection.connection_handler
def get_answer_by_question_id(cursor, question_id, order_criteria, order_direction):
    cursor.execute(f"""
                        SELECT * FROM answer
                        WHERE question_id = %(question_id)s
                        ORDER BY {order_criteria} {order_direction}
                        """,
                       {'question_id': question_id})
    return cursor.fetchall()
