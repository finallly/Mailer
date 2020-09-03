import logging
import configparser
import csv
from random import randrange
from threading import Thread
from aiogram import Bot, Dispatcher, executor, types

from sqlHandler import SQLHandler
from smtpConnect import smtpConnect
from errorHandling import errorHandler, SMTPDataError, SMTPAuthenticationError, SMTPConnectError, \
    SMTPServerDisconnected, SMTPSenderRefused

config = configparser.ConfigParser()
config.read('config.ini')

# TODO: maybe store configs in environment variables??

csv_file_name = config['DATA']['file_name']

reading_mode = config['DATA']['mode']
csv_delimiter = config['DATA']['delimiter']
server_address = config['DATA']['server']
csv_encoding = config['DATA']['encoding']
mail_address_index = int(config['DATA']['mail_index'])
mail_password_index = int(config['DATA']['password_index'])

database_host = config['DATA']['db_host']
database_user = config['DATA']['db_user']
database_pass = config['DATA']['db_pass']
database_name = config['DATA']['db_name']
table_name = config['DATA']['table_name']

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config['TOKEN']['token'])
dispatcher = Dispatcher(bot)

database = SQLHandler(database_host, database_user, database_pass, database_name)
data = [_ for _ in csv.reader(open(csv_file_name, mode=reading_mode, encoding=csv_encoding), delimiter=csv_delimiter)]


def worker(message: str, to_email: str, mail_index: int) -> None:
    try:
        with smtpConnect(server_address, data[mail_index][mail_address_index],
                         data[mail_index][mail_password_index]) as server:
            server.sendmail(data[mail_index][mail_address_index], to_email,
                            message)
    except (
            SMTPDataError, SMTPAuthenticationError, SMTPConnectError, SMTPServerDisconnected,
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


@dispatcher.message_handler(commands=['test'])
async def send(message: types.Message):
    _, to_email, text, amount = message.text.split()

    database.add_record(table_name, message.from_user.username, (to_email, text, amount))

    await message.answer('test successful!')


if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True)
