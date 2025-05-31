import telebot
import logic
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

categories = []

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, '')
@bot.message_handler(content_types=['text'])
def text(message):
    filename = f'{message.from_user.id}.png'
    bot.send_chat_action(message.chat.id, 'upload_photo', timeout=20)
    logic.gen(filename, message.text)
    bot.send_photo(message.chat.id, open(filename, 'rb'))

bot.infinity_polling()