import telebot
from telebot import types
import info  # bot_token
import database
from random import randint
import datetime
import sniffer # convert link to token
# get api vk https://oauth.vk.com/authorize?client_id=6121396&scope=4534279&redirect_uri=https://oauth.vk.com/blank.html&display=page&response_type=token&revoke=1

def main():
    print(f"Бот запущен!")
    bot = telebot.TeleBot(info.bot_token)

    @bot.message_handler(commands=['start']) #создаем команду
    def start(message):
        try:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Как авторизоваться?")
            btn2 = types.KeyboardButton("Принцип работы")
            btn_link = types.InlineKeyboardButton("Получить API")
            btn_random = types.InlineKeyboardButton("Испытать удачу (1-6ч)")
            btn_balance = types.InlineKeyboardButton("Баланс")          
            btn_start = types.InlineKeyboardButton("Запуск")
            markup.add(btn1, btn2, btn_link, btn_random, btn_balance, btn_start)
            bot.send_message(message.chat.id, text="Привет, {0.first_name}! Я TeleBot для накрутки лайков в ВКонтакте".format(message.from_user), reply_markup=markup)
        except:
            print("ERROR START")
        

    @bot.message_handler(content_types='text')
    def message_reply(message):
        try:
            print(f"{datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')} {message.chat.id} - {message.text}")
            if ("access_token" in message.text):
                bot.send_message(message.chat.id, f"Ваш API токен привязан!\nВам было выдано 24ч за регистрацию аккаунта")
                access_token = sniffer.get_link(message.text)
                database.create_task([message.chat.id, access_token, 24, -1])
                database.update_task([access_token, message.chat.id])
                print(f"Новый зарегестрированный пользователь! {message.chat.id}")

            elif (message.text == "Как авторизоваться?"):
                bot.send_message(message.chat.id, "1) Нажмите на 'Получить API'\n2) Скопируйте ссылку страницы\n3) Отправьте её боту\nВступайте в чат и задавайте вопросы напрямую админу\n@telebotlike")

            elif (message.text == "Получить API"):
                bot.send_message(message.chat.id, "Ссылка для получения API ключа https://goo.su/3ZJnc2\n")
                img = open('link.png', 'rb')
                bot.send_photo(message.chat.id, photo= img)
            elif (message.text == "Испытать удачу (1-6ч)"):
                database.add_balance(message.chat.id, randint(1, 6))
            elif (message.text == "Баланс"):
                bot.send_message(message.chat.id, f"Ваш баланс {database.check_balance(message.chat.id)}")
            elif (message.text == "Запуск"):
                bot.send_message(message.chat.id, f"С вашего баланса было снято {database.check_balance(message.chat.id)}\nНакрутка будет запущена в течении часа, убедитесь что вы ввели API ключ\n")
                database.launch_farm(message.chat.id)
            elif (message.text == "Принцип работы"):
                bot.send_message(message.chat.id, "От вашего именни в разные группы отправляются сообщения. Настоящие люди заходят и ставят вам лайки. ")
                media_group = []
                text = 'Example'
                for num in range(1,5):
                    media_group.append(types.InputMediaPhoto(open('example%d.png' % num, 'rb'), 
                                                    caption = text if num == 0 else ''))
                bot.send_media_group(chat_id = message.chat.id, media = media_group)
            else:
                bot.send_message(message.chat.id, text="На такую комманду я не запрограммировал..")
        except:
            print("ERROR REPLY")
    try:
        bot.infinity_polling()
    except:
        print("ERROR POOLING")

while True:
    try:
        main()
    except:
        pass


# datetime.datetime.today().weekday()