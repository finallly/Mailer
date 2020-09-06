import mysql.connector as mysql
from configparser import ConfigParser


class SqlHandler(object):

    def __init__(self):
        self.connection = mysql.connect(
            host=ConfigParser.database_host,
            user=ConfigParser.database_user,
            passwd=ConfigParser.database_pass,
            database=ConfigParser.database_name,
            auth_plugin=ConfigParser.auth_plugin
        )

    def __enter__(self):
        return self.connection.cursor()

    def __exit__(self, *args):
        self.connection.commit()
        self.connection.close()
