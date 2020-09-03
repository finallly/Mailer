import mysql.connector as mysql


class SqlHandler(object):

    def __init__(self, host, user, password, database):
        self.connection = mysql.connect(
            host=host,
            user=user,
            passwd=password,
            database=database
        )

    def __enter__(self):
        return self.connection.cursor()

    def __exit__(self, *args):
        self.connection.commit()
        self.connection.close()