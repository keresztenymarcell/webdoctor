import re
import connection, bcrypt
from werkzeug.utils import secure_filename
from datetime import datetime

import dh_general
import dh_python_files


@connection.connection_handler
def check_if_new_user(cursor, user_name):
    query = """
            SELECT * FROM users
            WHERE email = %(user_name)s
            """
    cursor.execute(query, {'user_name': user_name})
    user = cursor.fetchone()
    return True if user is None else False


def hash_password(plain_text_password):
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


@connection.connection_handler
def register_user(cursor, user_email, user_password, user_name):
    timestamp = dh_python_files.generate_timestamp()
    hashed_password = hash_password(user_password)
    query = """
                INSERT INTO users(user_name, password, email, reputation, registration_date, questions_count, answers_count, comments_count)
                VALUES(%s, %s, %s, 0, %s, 0, 0, 0)
                """
    cursor.execute(query, (user_name, hashed_password, user_email, timestamp))


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)


@connection.connection_handler
def get_user_password(cursor, user_info):
    query = """
            SELECT password FROM users
            WHERE email = %(user_email)s
            """
    cursor.execute(query, {'user_email': user_info['email']})
    return cursor.fetchone()


@connection.connection_handler
def get_user_data(cursor):
    query = """
            SELECT *
            FROM users
            """
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def add_new_information_by_user(cursor, table, user_id, information):
    cursor.execute = f"""
                INSERT INTO {table} (user_id)
                VALUES({user_id}),
                WHERE id = {information['id']}),
                 {'id':information['id']})
                """


@connection.connection_handler
def get_user_id_by_mail(cursor, email):
    query = """
            SELECT id FROM users
            WHERE email = %(email)s
            """
    cursor.execute(query, {'email': email})
    return cursor.fetchone()
    
@connection.connection_handler
def update_user(cursor, column, user_id):
    query = f"""
            UPDATE users
            SET {column} = {column} + 1
            WHERE id = %(user_id)s
            """
    cursor.execute(query, {"user_id": user_id})    
    
    
    
@connection.connection_handler
def reputation_manager(cursor, target_table, identifier, increment): 
    cursor.execute(f"""
                    UPDATE users
                    SET reputation = reputation + %(increment)s
                    FROM {target_table}
                    WHERE {target_table}.user_id = users.id AND {target_table}.id = %(identifier)s
                       """,
                   {
                       'identifier': identifier,
                       'increment': increment,}
                   )    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
