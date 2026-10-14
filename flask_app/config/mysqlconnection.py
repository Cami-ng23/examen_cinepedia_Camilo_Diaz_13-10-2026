import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

class MySQLConnection:

    def __init__(self, db):
        self.db = db

    def query_db(self, query, data=None):
        connection = pymysql.connect(
            host=os.getenv("MYSQL_HOST", "localhost"),
            user=os.getenv("MYSQL_USER", "root"),
            password=os.getenv("MYSQL_PASSWORD", ""),
            database=self.db,
            cursorclass=pymysql.cursors.DictCursor
        )

        cursor = connection.cursor()

        try:
            cursor.execute(query, data or ())
            connection.commit()

            if query.strip().lower().startswith("select"):
                result = cursor.fetchall()
            else:
                result = cursor.lastrowid

        except Exception as e:
            connection.rollback()
            raise e

        finally:
            cursor.close()
            connection.close()

        return result
