import sqlite3 as sql
from typing import BinaryIO


class SQLHandler:

    def __init__(self, database_file):
        self.connection = sql.connect(database_file)
        self.cursor = self.connection.cursor()

    def add_user(self, user_name, status=True):
        with self.connection:
            self.cursor.execute("INSERT INTO 'users' ('user_name', 'is_active') VALUES (?, ?)",
                                (user_name, status))
            print('success!')
            self.connection.commit()

    def change_status(self, user_name, status):
        with self.connection:
            self.cursor.execute("UPDATE 'users' SET 'is_active' WHERE 'user_name' = ?", (status, user_name))

    def check_user(self, user_name):
        with self.connection:
            self.cursor.execute("SELECT * FROM 'users' WHERE 'user_name' = ?", (user_name, ))
            result = self.cursor.fetchall()
            print(result)

    def close_connection(self):
        self.connection.close()