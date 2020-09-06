from .context_handling import SqlHandler
from datetime import datetime
from .consts import Consts, Types
import json


class SQLHandler:

    @staticmethod
    def update_record(table: str, username: str, record: tuple) -> None:
        """
        adds data to database # FIXME: fix this retarded docstring
        :param table: table name
        :param username: ...
        :param record: data
        :return: None
        """

        # TODO: here must be error handling!!!

        with SqlHandler() as sql:
            sql.execute(f'SELECT info FROM {table} WHERE username = "{username}"')

            data, date = json.loads(sql.fetchall()[bool(False)][bool(False)]), datetime.now().strftime(
                Consts.date_format)
            now = datetime.now().strftime(Consts.time_format)
            if date in data:
                data[date] += [[record[0], record[1], record[2], now]]
            else:
                data[date] = [[record[0], record[1], record[2], now]]

            sql.execute(f"UPDATE {table} SET info = '{json.dumps(data)}' WHERE username = '{username}'")

    @staticmethod
    def add_user(table: str, nametag: str, username: str) -> None:
        """
        # TODO: docstring here!
        :param table:
        :param nametag:
        :param username:
        :return: None
        """
        with SqlHandler() as sql:
            sql.execute(f"INSERT INTO {table} ({Consts.nametag}, {Consts.username}, "
                        f"{Consts.info}, {Consts.status}) VALUE (?, ?, ?, ?)",
                        (nametag, username, Types.json_dict, False))

    @staticmethod
    def change_status(table: str, username: str, status: bool) -> None:
        """
        # TODO: add here!
        :param table:
        :param username:
        :param status:
        :return:
        """
        with SqlHandler() as sql:
            sql.execute(f"UPDATE {table} SET status = {status} WHERE username = '{username}'")
