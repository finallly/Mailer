from .context_handling import SqlHandler
from datetime import datetime
from .consts import Consts, Types
import json


class SQLHandler:

    @staticmethod
    def update_record(table: str, id: int, record: list) -> None:
        """
        adds data to database # FIXME: fix this retarded docstring
        :param id:
        :param table: table name
        :param record: data
        :return: None
        """

        # TODO: here must be error handling!!!

        with SqlHandler() as sql:
            sql.execute(f'SELECT {Consts.info} FROM {table} WHERE {Consts.id} = "{id}"')

            data, date = json.loads(sql.fetchall()[bool(False)][bool(False)]), datetime.now().strftime(
                Consts.date_format)
            now = datetime.now().strftime(Consts.time_format)
            if date in data:
                data[date] += [[now, record]]
            else:
                data[date] = [[now, record]]

            sql.execute(f"UPDATE {table} SET {Consts.info} = '{json.dumps(data)}' WHERE {Consts.id} = '{id}'")

    @staticmethod
    def add_user(table: str, first: str, last: str, username: str, id: int) -> None:
        """
        # TODO: docstring here!
        :param id:
        :param first:
        :param last:
        :param table:
        :param username:
        :return: None
        """
        with SqlHandler() as sql:
            sql.execute(
                f"INSERT INTO {table} ({Consts.first_name}, {Consts.last_name}, {Consts.username}, {Consts.info}, "
                f"{Consts.status}, {Consts.id}, {Consts.is_blocked}) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (first, last, username, Types.json_dict, False, id, False))

    @staticmethod
    def change_status(table: str, id: int, status: bool) -> None:
        """
        # TODO: add here!
        :param id:
        :param table:
        :param status:
        :return:
        """
        with SqlHandler() as sql:
            sql.execute(f"UPDATE {table} SET {Consts.status} = {status} WHERE {Consts.id} = '{id}'")

    @staticmethod
    def check_user(table: str, id: int) -> bool:
        """

        :param id:
        :param table:
        :return:
        """
        with SqlHandler() as sql:
            sql.execute(f"SELECT * FROM {table} WHERE {Consts.id} = '{id}'")
            result = sql.fetchall()
            return bool(len(result))

    @staticmethod
    def get_user_info(table: str, id: int) -> None:
        """

        :param table:
        :param id:
        :return:
        """
        with SqlHandler() as sql:
            sql.execute(f"SELECT {Consts.info} FROM {table} WHERE {Consts.id} = '{id}'")
            result = sql.fetchall()

    @staticmethod
    def check_user_status(table: str, id: int) -> bool:
        """

        :param table:
        :param id:
        :return:
        """
        with SqlHandler() as sql:
            sql.execute(f"SELECT {Consts.status} FROM {table} WHERE {Consts.id} = '{id}'")
            result = bool(int(sql.fetchall()[0][0]))
            return result

    @staticmethod
    def block_user(table: str, id: int):
        """

        :param table:
        :param id:
        :return:
        """
        with SqlHandler() as sql:
            sql.execute(f"UPDATE {table} SET {Consts.is_blocked} = {True} WHERE {Consts.id} = '{id}'")
