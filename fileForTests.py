# import logging
# import smtplib
# from sqlHandler import SQLHandler
#
# from aiogram import Bot, Dispatcher, executor, types
#
# logging.basicConfig(level=logging.INFO)
# bot = Bot(token='999223265:AAFjOnam5HWc4CfJR78YFwF_r6SSGNyWWWc')
# dispatcher = Dispatcher(bot)
#
# fromemail = 'testmailforspamm@mail.ru'
# password = 'faksjflkj2348726234SDF'
# smtpserver = 'smtp.mail.ru:587'
#
# database = SQLHandler('userDataBase')
#
#
# @dispatcher.message_handler(commands=['join'])
# async def add_new_user(message: types.Message):
#     if not database.check_user(message.from_user.username):
#         database.add_user(message.from_user.username)
#         await message.answer('join successful')
#
#     else:
#         await message.answer('ure already in')
#
#
# @dispatcher.message_handler(commands=['leave'])
# async def change_user_state(message: types.Message):
#
#     database.change_status(message.from_user.username, False)
#
#     await message.answer('leave successful!')
#
#     # TODO: maybe put these 2 commands in one dispatcher?
#
#
# @dispatcher.message_handler(commands=['send'])
# async def start_spam(message: types.Message):
#     if not database.check_user(message.from_user.username):
#         await message.answer('you need to join')
#
#     _, to_email, text, amount = message.text.split()
#
#     server = smtplib.SMTP(smtpserver)
#     server.starttls()
#     server.login(fromemail, password)
#
#     # TODO: create additional file, which start the SMTP server and creates connections
#
#     for _ in range(int(amount)):
#         server.sendmail(fromemail, to_email, text)
#     server.quit()
#
#     await message.answer(f'{amount} email to {to_email} were sent!')
#
#
# if __name__ == '__main__':
#     executor.start_polling(dispatcher, skip_updates=True)


