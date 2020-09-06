from .context_handling import SqlHandler
from datetime import datetime
from .consts import Consts, Types
import json


class SQLHandler:

    @staticmethod
    def update_record(table: str, username: str, record: list) -> None:
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
                data[date] += [[now, record]]
            else:
                data[date] = [[now, record]]

            sql.execute(f"UPDATE {table} SET info = '{json.dumps(data)}' WHERE username = '{username}'")

    @staticmethod
    def add_user(table: str, first: str, last: str,  username: str) -> None:
        """
        # TODO: docstring here!
        :param first:
        :param last:
        :param table:
        :param username:
        :return: None
        """
        with SqlHandler() as sql:
            sql.execute(f"INSERT INTO {table} ({Consts.first_name}, {Consts.last_name}, {Consts.username}, "
                        f"{Consts.info}, {Consts.status}) VALUES (%s, %s, %s, %s, %s)",
                        (first, last, username, Types.json_dict, False))

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

    @staticmethod
    def check_user(table: str, username: str) -> bool:
        """

        :param table:
        :param username:
        :return:
        """
        with SqlHandler() as sql:
            sql.execute(f"SELECT * FROM {table} WHERE username = '{username}'")
            result = sql.fetchall()
            return bool(len(result))

    @staticmethod
    def get_user_info(table: str, username: str) -> None:
        with SqlHandler() as sql:
            sql.execute(f"SELECT info FROM {table} WHERE username = '{username}'")
            result = sql.fetchall()



