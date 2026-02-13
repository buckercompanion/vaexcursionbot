import telebot
import os
from telebot import types

# Берем токен из переменных окружения Bothost
TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# Словарь для связи названия кнопки с её номером
LOCATIONS = {
    'Красивые места': 1,
    'Офигенные места': 2,
    'Прекрасные места': 3,
    'Клевые места': 4
}

def main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Создаем кнопки из ключей нашего словаря
    buttons = [types.KeyboardButton(text) for text in LOCATIONS.keys()]
    # Добавляем их в разметку по 2 в ряд
    markup.add(buttons[0], buttons[1])
    markup.add(buttons[2], buttons[3])
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id, 
        "Привет! Выбери интересующую локацию:", 
        reply_markup=main_keyboard()
    )

@bot.message_handler(content_types=['text'])
def handle_location(message):
    # Проверяем, есть ли такой текст среди наших кнопок
    if message.text in LOCATIONS:
        button_number = LOCATIONS[message.text]
        media_group = []
        
        # Цикл от 1 до 5 для поиска существующих фото
        for i in range(1, 6):
            file_path = f'images/photo_{button_number}_{i}.jpg'
            
            # Проверяем, существует ли файл, чтобы бот не «упал» с ошибкой
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    # Для первого фото в группе можно добавить подпись (название кнопки)
                    caption = message.text if len(media_group) == 0 else ""
                    media_group.append(types.InputMediaPhoto(f.read(), caption=caption))
        
        # Если нашли хотя бы одно фото — отправляем
        if media_group:
            bot.send_chat_action(message.chat.id, 'upload_photo')
            bot.send_media_group(message.chat.id, media_group)
        else:
            bot.send_message(message.chat.id, "Фотографии для этого раздела скоро появятся!")
    else:
        bot.send_message(message.chat.id, "Пожалуйста, используйте кнопки меню.")

# Запуск
if __name__ == '__main__':
    bot.polling(none_stop=True)
