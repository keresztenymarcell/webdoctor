import re
import connection, bcrypt
from werkzeug.utils import secure_filename
from datetime import datetime

@connection.connection_handler
def insert_tag(target_indices, datatable, entry_index, key, phrase, tag_type):
    count = 0
    for start in target_indices:
        result = list(datatable[entry_index][key])
        result.insert((start + count * (len(f'<{tag_type}>') + len(f'</{tag_type}>'))), f'<{tag_type}>')
        result.insert((start + (count * (len(f'<{tag_type}>') + len(f'</{tag_type}>'))) + 1 + len(phrase)), f'</{tag_type}>')
        result = ''.join(result)
        datatable[entry_index][key] = result
        count += 1


@connection.connection_handler
def get_all_tag(cursor):
    cursor.execute("""
                    SELECT * FROM tag
                    """)
    return cursor.fetchall()
  
  
@connection.connection_handler
def filter_tags(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM tag
                    FULL OUTER JOIN question_tag
                    ON tag.id = question_tag.tag_id
                    WHERE question_tag.question_id != %(question_id)s
                    """, {'question_id': question_id})
    return cursor.fetchall()
    
    
    
@connection.connection_handler
def add_new_tag(cursor, tag_name):
    cursor.execute("""
                        INSERT INTO tag (name)
                        VALUES(%(tag_name)s) RETURNING id;
                        """, {'tag_name': tag_name})
    return cursor.fetchone()



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
def add_tag_id_to_question_tag(cursor, tag_id, question_id):
    cursor.execute("""
                        INSERT INTO question_tag(question_id, tag_id)
                        VALUES(%(question_id)s, %(tag_id)s)
                        """,
                        {'question_id': question_id, 'tag_id': tag_id})


@connection.connection_handler
def get_tags_by_question_id(cursor, question_id):
    cursor.execute("""
                    SELECT id, name FROM tag
                    RIGHT OUTER JOIN question_tag
                    ON tag.id = question_tag.tag_id
                    WHERE question_id = %(question_id)s
                    
                    """, {'question_id': question_id})
    return cursor.fetchall()

                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
