import logging
import smtplib

from aiogram import Bot, Dispatcher, executor, types

logging.basicConfig(level=logging.INFO)
bot = Bot(token='999223265:AAFjOnam5HWc4CfJR78YFwF_r6SSGNyWWWc')
dispatcher = Dispatcher(bot)

fromemail = 'testmailforspamm@mail.ru'
password = 'faksjflkj2348726234SDF'
smtpserver = 'smtp.mail.ru:587'

server = smtplib.SMTP(smtpserver)
server.starttls()
server.login(fromemail, password)


@dispatcher.message_handler()
async def echo(message: types.Message):
    # await message.answer(f'write command with the same arguments - target_mail_address message amount_of_mails')

    to_email, text, amount = message.text.split()

    for _ in range(int(amount)):
        server.sendmail(fromemail, to_email, text)
    server.quit()

    await message.answer(f'{amount} email to {to_email} were sent!')


if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True)


# import socket
#
# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# server_socket.bind(('localhost', 5000))
# server_socket.listen()
#
# flag = True
#
# while flag:
#     client_socket, address = server_socket.accept()
#     print('connection set')
#
#     while True:
#         try:
#             request = client_socket.recv(1024).strip()
#         except ConnectionResetError as error:
#             print(str(error))
#             break
#
#         if not request:
#             flag = not flag
#             print('message is empty')
#             break
#         else:
#             response = 'hello\n' + str(address) + '\n'
#             response = response.encode() + request
#             client_socket.send(response)