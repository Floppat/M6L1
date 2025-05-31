import logic
import telebot
from config import TOKEN
import random, schedule, time, requests, threading, os

bot = telebot.TeleBot(TOKEN)

categories = ['аниме','черно-белый', 'диснеевский мультик', 'кавказский']

id = 0

@bot.message_handler(commands=['start'])
def strt(message):
    global id
    id = message.chat.id
    bot.send_message(message.chat.id, 'привет напиши что угодно и я сгенерирую изображение по тексту')


count = 25
status = False
id_message = 0
@bot.message_handler(content_types=['text'])
def text(message):
    global count, status, id_message, id
    count = 25
    id = message.chat.id
    id_message = bot.send_message(message.chat.id,'осталось: ' + str(count) + " сек.").message_id
    status = True
    filename = f'{message.from_user.id}.png'
    bot.send_chat_action(message.chat.id,'upload_photo')
    logic.generate_image(filename, message.text)
    bot.send_photo(message.chat.id, open(filename, 'rb'))
    status = False
    bot.delete_message(message.chat.id, id_message)
    os.remove(filename)




def task():
    global status, count, id_message
    if status:
        count -= 1
        bot.edit_message_text(chat_id=id, message_id=id_message, text='осталось: ' + str(count) + " сек.")


def check_time():
    schedule.every(1).seconds.do(task)
    while True:
        schedule.run_pending() # Вызываем все задачи, время которых подошло
        time.sleep(1)

def start_bot():
    bot.infinity_polling()


threading.Thread(target=start_bot).start()
threading.Thread(target=check_time).start()
