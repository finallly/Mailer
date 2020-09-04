from .context_handling import SqlHandler
from datetime import datetime
from .consts import Consts
import json


class SQLHandler:

    def __init__(self, host: str, user: str, password: str, database: str):
        self.host = host
        self.user_name = user
        self.password = password
        self.database = database

    def update_record(self, table: str, username: str, record: tuple) -> None:
        """
        adds data to database # FIXME: fix this retarded docstring
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
                Consts.date_format)
            now = datetime.now().strftime(Consts.time_format)
            if date in data:
                data[date] += [[record[0], record[1], record[2], now]]
            else:
                data[date] = [[record[0], record[1], record[2], now]]

            sql.execute(f"UPDATE {table} SET info = '{json.dumps(data)}' WHERE username = '{username}'")

    def add_user(self, table: str, nametag: str, username: str) -> None:
        """
        # TODO: docstring here!
        :param table:
        :param nametag:
        :param username:
        :return: None
        """
        with SqlHandler(
                self.host,
                self.user_name,
                self.password,
                self.database
        ) as sql:
            sql.execute(f"INSERT INTO {table} ({Consts.nametag}, {Consts.username}, {Consts.info}) VALUE (?, ?, ?)",
                        (nametag, username))
