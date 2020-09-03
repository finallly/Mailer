from .context_handling import SqlHandler
from datetime import datetime
import json


class SQLHandler:

    def __init__(self, host: str, user: str, password: str, database: str):
        self.host = host
        self.user_name = user
        self.password = password
        self.database = database

    def add_record(self, table: str, username: str, record: tuple):
        """
        adds data to database
        :param table: table name
        :param username: ...
        :param record: data
        :return: None
        """

        # TODO: here must be error handling!!!

        with SqlHandler(
                self.host,
                self.user_name,
                self.password,
                self.database
        ) as sql:
            sql.execute(f'SELECT info FROM {table} WHERE username = "{username}"')

            data, date = json.loads(sql.fetchall()[bool(False)][bool(False)]), datetime.now().strftime(
                "%d.%m.%Y-%H:%M:%S")
            if date in data:
                data[date] += [record[0], record[1], record[2]]
            else:
                data[date] = [record[0], record[1], record[2]]

            sql.execute(f"UPDATE {table} SET info = '{json.dumps(data)}' WHERE username = '{username}'")
