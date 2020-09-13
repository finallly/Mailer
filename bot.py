import logging
import csv
import requests
import ast

from random import randrange
from threading import Thread
from aiogram.dispatcher import FSMContext
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from sqlHandler import SQLHandler
from sqlHandler.consts import TYPES, CONSTS, STRINGS
from stateHandler import STATES
from smtpConnect import smtpConnect
from configHandler import ConfigHandler
from errorHandling import errorHandler, SMTPDataError, SMTPAuthenticationError, SMTPConnectError, \
    SMTPServerDisconnected, SMTPSenderRefused

logging.basicConfig(level=logging.INFO)
bot = Bot(token=ConfigHandler.token)
dispatcher = Dispatcher(bot, storage=MemoryStorage())

database = SQLHandler()

data = [_ for _ in csv.reader(
    open(ConfigHandler.csv_file_name, mode=ConfigHandler.reading_mode, encoding=ConfigHandler.csv_encoding),
    delimiter=ConfigHandler.csv_delimiter)]


# def worker(message: str, to_email: str, mail_index: int) -> None:
#     try:
#         with smtpConnect(ConfigHandler.server_address, data[mail_index][ConfigHandler.mail_address_index],
#                          data[mail_index][ConfigHandler.mail_password_index]) as server:
#             server.sendmail(data[mail_index][ConfigHandler.mail_address_index], to_email,
#                             message)
#     except (SMTPDataError, SMTPAuthenticationError, SMTPConnectError, SMTPServerDisconnected,
#             SMTPSenderRefused) as error:
#         errorHandler(error)
#
#
# def thread_gen(count: int, func, to_email: str, text: str) -> None:
#     database_indexes = [randrange(len(data)) for _ in range(count)]
#
#     threads = [
#         Thread(target=func, args=(text, to_email, index)) for index in database_indexes
#     ]
#     for thread in threads:
#         thread.start()
#     for thread in threads:
#         thread.join()


@dispatcher.message_handler(commands=['start'])
async def start(message: types.Message):
    keyboard = [
        [
            types.KeyboardButton(TYPES.button_start),
            types.KeyboardButton(TYPES.button_services_count)
        ],
        [
            types.KeyboardButton(TYPES.button_info),
            types.KeyboardButton(TYPES.button_contact)
        ]
    ]

    if message.from_user.id in ast.literal_eval(ConfigHandler.admins):
        keyboard.append(
            [
                types.KeyboardButton(TYPES.button_change),
                types.KeyboardButton(TYPES.button_block),
            ]
        )

    if not database.check_user(ConfigHandler.table_name, message.from_user.id):
        database.add_user(ConfigHandler.table_name, message.from_user.first_name,
                          message.from_user.last_name, message.from_user.username, message.from_user.id)

    markup = types.ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

    await message.answer('Greetings, traveller..', reply_markup=markup)


# @dispatcher.message_handler(commands=Types.admin_commands)
# async def admin_handler(message: types.Message):
#     text = message.text.split(' ')
#


@dispatcher.message_handler(content_types=['text'], state=None)
async def button_recognizer(message: types.Message):
    if message.text == TYPES.button_start:
        await message.answer("enter the number with format:\n+7XXXXXXXXXX")
        await STATES.bombing.set()

    elif message.text == TYPES.button_services_count:
        result = requests.get(
            ConfigHandler.status_link, params=TYPES.params_dict
        ).json()
        count = result.get('count')
        await message.answer(f"available services count: {count}")

    elif message.text == TYPES.button_info:
        await message.answer(STRINGS.info_string)

    elif message.text == TYPES.button_contact:
        await message.answer(STRINGS.contact_string)

    elif message.text == TYPES.button_change:
        await STATES.changing.set()

    elif message.text == TYPES.button_block:
        await STATES.blocking.set()


@dispatcher.message_handler(state=STATES.bombing)
async def start_bombing(message: types.Message, state: FSMContext):
    try:
        text = message.text.split(' ')
        count = int(text[CONSTS.command_second])

        if not database.check_user_status(ConfigHandler.table_name, message.from_user.id):
            count = CONSTS.base_laps_count

        response = requests.post(
            ConfigHandler.attack_link,
            json={ConfigHandler.api_number: count,
                  ConfigHandler.api_phone: text[CONSTS.command_first]},
        ).json()

        database.update_record(ConfigHandler.table_name, message.from_user.id,
                               text[CONSTS.command_first])

        status = response.get('success')
        identifier = response.get('id')
        await state.update_data(id=identifier)

        inline_markup = types.InlineKeyboardMarkup(
            [
                types.InlineKeyboardButton(text=TYPES.button_status, callback_data=TYPES.callback_status),
                types.InlineKeyboardButton(text=TYPES.button_stop, callback_data=TYPES.callback_stop)
            ]
        )
        # button_status = types.InlineKeyboardButton(text=TYPES.button_status, callback_data=TYPES.callback_status)
        # button_stop = types.InlineKeyboardButton(text=TYPES.button_stop, callback_data=TYPES.callback_stop)
        # inline_markup.add(button_status, button_stop)

        if status:
            await message.answer(f"attack to {text[CONSTS.command_first]}", reply_markup=inline_markup)
        else:
            await message.answer(f"error, try again")

    except (IndexError, ValueError, TypeError) as error:
        errorHandler(error)
        await message.answer('cancel')

    finally:
        await state.finish()


@dispatcher.message_handler(state=STATES.changing)
async def change_subscription_status(message: types.Message, state: FSMContext):
    try:
        text = message.text.split(' ')
        database.change_status(ConfigHandler.table_name, text[CONSTS.command_first],
                               bool(int(text[CONSTS.command_second])))
        await message.answer(f'{text[CONSTS.command_first]} status changed')

    except (IndexError, ValueError, TypeError) as error:
        errorHandler(error)
        await message.answer('cancel')

    finally:
        await state.finish()


@dispatcher.message_handler(state=STATES.blocking)
async def block_user(message: types.Message, state: FSMContext):
    try:
        text = message.text.split(' ')
        database.block_user(ConfigHandler.table_name, text[CONSTS.command_first])
        await message.answer(f'user {text[CONSTS.command_first]} blocked')

    except (IndexError, ValueError, TypeError) as error:
        errorHandler(error)
        await message.answer('cancel')

    finally:
        await state.finish()


@dispatcher.callback_query_handler(lambda call: call.data == TYPES.button_status)
async def inline_handling(callback_query: types.CallbackQuery):
    print('feck')
    await callback_query.answer('test inline button')


if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True)
