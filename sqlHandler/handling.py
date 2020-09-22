from .context_handling import SqlHandler
from datetime import datetime
from .consts import CONSTS, TYPES
import json


class SQLHandler:

    @staticmethod
    def update_record(table: str, id: int, record: str) -> None:
        """
        this method updates information that user gave to bot
        :param table: sql table name
        :param id: user telegram id
        :param record: new record
        :return: None
        """

        # TODO: here must be error handling!!!

        with SqlHandler() as sql:
            sql.execute(f'SELECT {CONSTS.info} FROM {table} WHERE {CONSTS.id} = "{id}"')

            data, date = json.loads(sql.fetchall()[bool(False)][bool(False)]), datetime.now().strftime(
                CONSTS.date_format)
            now = datetime.now().strftime(CONSTS.time_format)
            if date in data:
                data[date] += [[now, record]]
            else:
                data[date] = [[now, record]]

            sql.execute(f"UPDATE {table} SET {CONSTS.info} = '{json.dumps(data)}' WHERE {CONSTS.id} = '{id}'")

    @staticmethod
    def add_user(table: str, first: str, last: str, username: str, id: int) -> None:
        """
        this method adds new user to database
        :param table: sql table name
        :param first: user telegram first name
        :param last: user telegram last name
        :param id: user telegram id
        :param username: user`s telegram username
        :return: None
        """
        with SqlHandler() as sql:
            sql.execute(
                f"INSERT INTO {table} ({CONSTS.first_name}, {CONSTS.last_name}, {CONSTS.username}, {CONSTS.info}, "
                f"{CONSTS.status}, {CONSTS.id}, {CONSTS.is_blocked}) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (first, last, username, TYPES.json_dict, False, id, False))

    @staticmethod
    def change_status(table: str, id: int, status: bool) -> None:
        """
        this method changes user`s status to VIP or back
        :param table: sql table name
        :param id: user telegram id
        :param status: new user status
        :return: None
        """
        with SqlHandler() as sql:
            sql.execute(f"UPDATE {table} SET {CONSTS.status} = {status} WHERE {CONSTS.id} = '{id}'")

    @staticmethod
    def check_user(table: str, id: int) -> bool:
        """
        this method checks if user is already in database
        :param table: sql table name
        :param id: user telegram id
        :return: True or False
        """
        with SqlHandler() as sql:
            sql.execute(f"SELECT * FROM {table} WHERE {CONSTS.id} = '{id}'")
            result = sql.fetchall()
            return bool(len(result))

    @staticmethod
    def get_user_info(table: str, id: int) -> None:
        """
        this method shows user`s activity
        :param table: sql table name
        :param id: user telegram id
        :return: None
        """
        with SqlHandler() as sql:
            sql.execute(f"SELECT {CONSTS.info} FROM {table} WHERE {CONSTS.id} = '{id}'")
            result = sql.fetchall()

    @staticmethod
    def check_user_status(table: str, id: int) -> bool:
        """
        this method checks that the user has VIP status
        :param table: sql table name
        :param id: user telegram id
        :return: True of False
        """
        with SqlHandler() as sql:
            sql.execute(f"SELECT {CONSTS.status} FROM {table} WHERE {CONSTS.id} = '{id}'")
            result = bool(int(sql.fetchall()[0][0]))
            return result

    @staticmethod
    def block_user(table: str, id: int) -> None:
        """
        this method adds user`s id to block list so he cant change his username or name to access the bot
        :param table: sql table name
        :param id: user telegram id
        :return: None
        """
        with SqlHandler() as sql:
            sql.execute(f"UPDATE {table} SET {CONSTS.is_blocked} = {True} WHERE {CONSTS.id} = '{id}'")

    @staticmethod
    def check_block(table: str, id: int) -> bool:
        """
        this method checks if user is banned
        :param table: sql table name
        :param id: user telegram id
        :return: True of False
        """
        with SqlHandler() as sql:
            sql.execute(f"SELECT {CONSTS.is_blocked} FROM {table} WHERE {CONSTS.id} = '{id}'")
            result = bool(int(sql.fetchall()[0][0]))
            return result
