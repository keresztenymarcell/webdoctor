
import connection


import dh_python_files


@connection.connection_handler
def edit_comment(cursor, comment_id, edited):
    timestamp = dh_python_files.generate_timestamp()
    cursor.execute("""
                    UPDATE comment
                    SET message = %(message)s,
                        submission_time = %(timestamp)s, edited_count = edited_count + 1
                    WHERE id = %(id)s
                    """,
                   {'message': edited['message'], 'timestamp': timestamp, 'id': comment_id})



@connection.connection_handler
def add_new_comment(cursor, comment_dict):
    timestamp = dh_python_files.generate_timestamp()
    cursor.execute("""
                        INSERT INTO comment(question_id, answer_id, message, submission_time, edited_count, user_id)
                        VALUES(%(question_id)s, %(answer_id)s, %(message)s, %(submission_time)s, %(edited_count)s, %(user_id)s);
                        """,
                       {'question_id': comment_dict['question_id'],
                        'answer_id': comment_dict['answer_id'],
                        'message': comment_dict['message'],
                        'submission_time': timestamp,
                        'edited_count': comment_dict['edited_count'],
                        'user_id': comment_dict['user_id']})




@connection.connection_handler
def get_comment_by_question_id(cursor, question_id):
    cursor.execute("""
                        SELECT id, message, submission_time, edited_count FROM comment
                        WHERE question_id = %(question_id)s
                        """,
                       {'question_id': question_id})
    return cursor.fetchall()

