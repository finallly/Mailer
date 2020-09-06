import mysql.connector as mysql
from configHandler import ConfigHandler


class SqlHandler(object):

    def __init__(self):
        self.connection = mysql.connect(
            host=ConfigHandler.database_host,
            user=ConfigHandler.database_user,
            passwd=ConfigHandler.database_pass,
            database=ConfigHandler.database_name,
            auth_plugin=ConfigHandler.auth_plugin
        )

    def __enter__(self):
        return self.connection.cursor()

    def __exit__(self, *args):
        self.connection.commit()
        self.connection.close()
