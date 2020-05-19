import telebot

bot = telebot.TeleBot('1280205698:AAG_FTfnSt9p2Ag05xJoVEX6dAULUn92kCg')


@bot.message_handler(content_types=['text'])
def fuck(message):
    bot.send_message(message.chat.id, message.text)


bot.polling(none_stop=True, timeout=123)
