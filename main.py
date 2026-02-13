import telebot
import os
from telebot import types

# Берем токен из переменных окружения, которые ты указал в Bothost
TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# Создаем клавиатуру
def main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Мельковская площадь')
    btn2 = types.KeyboardButton('Уралгипротранс')
    btn3 = types.KeyboardButton('Мельковская улица')
    btn4 = types.KeyboardButton('Василий Еремин')
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Выбери локацию, чтобы увидеть фото:", reply_markup=main_keyboard())

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == 'Мельковская площадь':
        # Отправляем группу из 3-х фото (альбомом)
        photos = [
            types.InputMediaPhoto('https://example.com/photo1.jpg', caption="Описание для всей группы"),
            types.InputMediaPhoto('https://example.com/photo2.jpg'),
            types.InputMediaPhoto('https://example.com/photo3.jpg')
        ]
        bot.send_media_group(message.chat.id, photos)
    
    elif message.text == 'Уралгипротранс':
        # Можно отправить просто текстом или другими фото
        bot.send_message(message.chat.id, "Тут будут фото Уралгипротранса")
    
    # И так далее для остальных кнопок...

bot.polling(none_stop=True)