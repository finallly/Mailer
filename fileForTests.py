import logging
import configparser
import csv
from random import randrange
from threading import Thread
from aiogram import Bot, Dispatcher, executor, types

from sqlHandler import SQLHandler
from smtpConnect import smtpConnect

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

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config['TOKEN']['token'])
dispatcher = Dispatcher(bot)

database = SQLHandler('userDataBase')
data = [_ for _ in csv.reader(open(csv_file_name, mode=reading_mode, encoding=csv_encoding), delimiter=csv_delimiter)]


def worker(message: str, to_email: str, mail_index: int) -> None:
    with smtpConnect(server_address, data[mail_index][mail_address_index],
                     data[mail_index][mail_password_index]) as server:
        server.sendmail(data[mail_index][mail_address_index], to_email,
                        message)


def thread_gen(count: int, func, to_email: str, text: str) -> None:
    database_indexes = [randrange(0, len(data)) for _ in range(count)]

    threads = [
        Thread(target=func, args=(text, to_email, index)) for index in database_indexes
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


@dispatcher.message_handler(commands=['join'])
async def add_new_user(message: types.Message):
    if not database.check_user(message.from_user.username):
        database.add_user(message.from_user.username)
        await message.answer('join successful')

    else:
        database.change_status(message.from_user.username, True)
        await message.answer('ure already in')


@dispatcher.message_handler(commands=['leave'])
async def change_user_state(message: types.Message):
    database.change_status(message.from_user.username, False)

    await message.answer('leave successful!')

    # TODO: maybe put these 2 commands in one dispatcher?


@dispatcher.message_handler(commands=['send'])
async def start_spam(message: types.Message):
    if not database.check_user(message.from_user.username):
        await message.answer('you need to join')

    _, to_email, text, amount = message.text.split()

    thread_gen(int(amount), worker, to_email, text)

    await message.answer(f'{amount} email to {to_email} were sent!')


if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True)
