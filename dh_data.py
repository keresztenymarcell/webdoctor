import re
import connection, bcrypt
from werkzeug.utils import secure_filename
from datetime import datetime

@connection.connection_handler
def get_all_data(cursor, table, order_by, direction):
    cursor.execute(f"""
                    SELECT * FROM {table}
                    ORDER BY {order_by} {direction}
                    """)

    return cursor.fetchall()
    
    
@connection.connection_handler
def get_data_by_id(cursor, table, data_id):
    cursor.execute(f"""
                    SELECT * FROM {table}
                    WHERE id = {data_id}
                    """)
    return cursor.fetchone()


def image_data_handling(UPLOAD_FOLDER, image_data, get_data, do_edit):
    if secure_filename(image_data.filename) != "":
        time = generate_timestamp()
        to_replace = {'-': '', ' ': '_', ':': ''}
        for key, value in to_replace.items():
            time = time.replace(key, value)
        get_data["image"] = time + "_" + secure_filename(image_data.filename)
        folder_route = UPLOAD_FOLDER + get_data["image"]
        image_data.save(folder_route)
    elif do_edit:
        pass
    else:
        get_data["image"] = ''


@connection.connection_handler
def delete_data_by_id(cursor, table, data_id):
    cursor.execute(f"""
                    DELETE from {table}
                    WHERE id = {data_id}
                   """)

