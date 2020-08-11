import sqlite3 as sql


class SQLHandler:

    # TODO: database format: uid, nametag, username, info: {'date': [('mail', 'text', count), ...]}

    def __init__(self, database_file):
        self.connection = sql.connect(database_file)
        self.cursor = self.connection.cursor()

    def add_user(self, user_name, status=True):
        with self.connection:
            self.cursor.execute("INSERT INTO 'users' ('user_name', 'is_active') VALUES (?, ?)",
                                (user_name, status))
            self.connection.commit()

    def change_status(self, user_name, status):
        # TODO: here i can rewrite the context manager!!!
        with self.connection:
            self.cursor.execute(f"UPDATE 'users' SET 'is_active' = {status} WHERE 'user_name' = '{user_name}'")
            print(status)
            self.connection.commit()

    def check_status(self, user_name):
        with self.connection:
            self.cursor.execute(f"SELECT 'is_active' FROM 'users' WHERE 'user_name' = '{user_name}'")
            return self.cursor.fetchall()

    def check_user(self, user_name):
        with self.connection:
            self.cursor.execute(f"SELECT * FROM users WHERE user_name = '{user_name}'")
            result = self.cursor.fetchall()
            return bool(len(result))

    def close_connection(self):
        self.connection.close()
