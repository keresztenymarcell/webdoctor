import connection


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


@connection.connection_handler
def delete_data_by_id(cursor, table, data_id):
    cursor.execute(f"""
                    DELETE from {table}
                    WHERE id = {data_id}
                   """)

