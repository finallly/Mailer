import logging
import csv
from random import randrange
from threading import Thread
from aiogram import Bot, Dispatcher, executor, types

from sqlHandler import SQLHandler
from smtpConnect import smtpConnect
from configHandler import ConfigHandler
from errorHandling import errorHandler, SMTPDataError, SMTPAuthenticationError, SMTPConnectError, \
    SMTPServerDisconnected, SMTPSenderRefused

logging.basicConfig(level=logging.INFO)
bot = Bot(token=ConfigHandler.token)
dispatcher = Dispatcher(bot)

database = SQLHandler()

data = [_ for _ in csv.reader(
    open(ConfigHandler.csv_file_name, mode=ConfigHandler.reading_mode, encoding=ConfigHandler.csv_encoding),
    delimiter=ConfigHandler.csv_delimiter)]


def worker(message: str, to_email: str, mail_index: int) -> None:
    try:
        with smtpConnect(ConfigHandler.server_address, data[mail_index][ConfigHandler.mail_address_index],
                         data[mail_index][ConfigHandler.mail_password_index]) as server:
            server.sendmail(data[mail_index][ConfigHandler.mail_address_index], to_email,
                            message)
    except (SMTPDataError, SMTPAuthenticationError, SMTPConnectError, SMTPServerDisconnected,
            SMTPSenderRefused) as error:
        errorHandler(error)


def thread_gen(count: int, func, to_email: str, text: str) -> None:
    database_indexes = [randrange(len(data)) for _ in range(count)]

    threads = [
        Thread(target=func, args=(text, to_email, index)) for index in database_indexes
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


@dispatcher.message_handler(commands=['test_up', 'test_add', 'test_change'])
async def send(message: types.Message):
    text = message.text.split(' ')
    if text[0] == '/test_up':
        database.update_record(ConfigHandler.table_name, message.from_user.username, text[1])
        await message.answer('test successful!')
    elif text[0] == '/test_add':
        if not database.check_user(ConfigHandler.table_name, message.from_user.username):
            print(message.from_user)
            database.add_user(ConfigHandler.table_name, message.from_user.first_name, message.from_user.last_name,
                              message.from_user.username)
            await message.answer('added successful')
        else:
            await message.answer('user already in database')
    elif text[0] == '/test_change':
        database.change_status(ConfigHandler.table_name, message.from_user.username, text[1])
        await message.answer('state changed successfully')

if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True)
