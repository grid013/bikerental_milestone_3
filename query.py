# import sqlite3
import psycopg2
from psycopg2 import Error
import os

def runQuery(query_str,query_type):
    result = []
    try:
        connection = psycopg2.connect(os.environ["DATABASE_URL"])
        cursor = connection.cursor()

        cursor.execute(query_str)
        if query_type == "insert":
            connection.commit()
        elif query_type == "select":
            columns = [col[0] for col in cursor.description]
            result = [dict(zip(columns, row)) for row in cursor.fetchall()]
        elif query_type == "update":
            connection.commit()
            result = cursor.rowcount

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

    return result
