import logging
import configparser
from sqlHandler import SQLHandler
from smtpConnect import smtpConnect

from aiogram import Bot, Dispatcher, executor, types

config = configparser.ConfigParser()
config.read('config.ini')

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config['TOKEN']['token'])
dispatcher = Dispatcher(bot)

database = SQLHandler('userDataBase')


@dispatcher.message_handler(commands=['join'])
async def add_new_user(message: types.Message):
    if not database.check_user(message.from_user.username):
        database.add_user(message.from_user.username)
        await message.answer('join successful')

    else:
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

    with smtpConnect(
        config['SERVER']['server'],
        config['SERVER']['from_mail'],
        config['SERVER']['password']
    ) as server:
        for _ in range(int(amount)):
            server.sendmail(config['SERVER']['from_mail'], to_email, text)

    await message.answer(f'{amount} email to {to_email} were sent!')


if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True)
