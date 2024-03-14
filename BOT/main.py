import telebot
import sqlite3
import os
import random
import webbrowser
from telebot import types
from telebot.types import InputMediaPhoto

# from aiogram.types import Message
# from telegram import InlineKeyboardButton, InlineKeyboardMarkup
# from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

TOKEN = 'rtrtrtrtrtrtrtrtrtrt'

bot = telebot.TeleBot(TOKEN)
CHAT_ID = 'YOUR_CHAT_ID'

conn = sqlite3.connect('BD//DataBot.db', check_same_thread=False)
cursor = conn.cursor()


def get_posts():
    with conn:
        cursor.execute("SELECT * FROM MailingSale")
        print(cursor.fetchall())
        cursor.execute("SELECT * FROM RootUsers")
        print(cursor.fetchall())
        cursor.execute(
            'select Contract.contact_number, Demand.FIO, Demand.address, Type_pay.Pay, Contract.sum, Executor.FIO, Status_work.status from Contract join Type_pay on Contract.id_type_pay = Type_pay.id join Status_work on Contract.id_status = Status_work.id join Demand on Contract.contact_number = Demand.contract_number join Executor on Executor.id = Demand.id_executor where Contract.contact_number == 12345').fetchall()
        print(cursor.fetchall())


get_posts()


@bot.message_handler(commands=['start'])
def start_menu(message):
    markup = types.ReplyKeyboardMarkup()
    btnsite = types.KeyboardButton('О компании')
    markup.row(btnsite)
    btnprs = types.KeyboardButton('Прайс-лист компании 🗒')
    markup.row(btnprs)
    btnstatus = types.KeyboardButton('Статус заказа')
    markup.row(btnstatus)
    btnsrc = types.KeyboardButton('Быть в курсе акцуий 🚨')
    markup.row(btnsrc)
    btn_support = types.KeyboardButton('Связь с оператором')
    markup.row(btn_support)
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!' \
                                      'Я бот компании по ремонту балконов. Чем я могу помочь? !', reply_markup=markup)
    # bot.register_next_step_handler(message, on_click)


@bot.message_handler(commands=['root_user'])
def admin_user(message):
    us_id = message.chat.id
    user = cursor.execute('SELECT * FROM RootUsers WHERE user_id=%d' % us_id).fetchall()
    if user:
        markup = types.ReplyKeyboardMarkup()
        btnsite = types.KeyboardButton('Добавить заказ')
        markup.row(btnsite)
        btnprs = types.KeyboardButton('Удалить заказ')
        btnsrc = types.KeyboardButton('Изменение заказа')
        btnstatus = types.KeyboardButton('Статус заказа')
        markup.row(btnprs, btnsrc, btnstatus)
        btnback = types.KeyboardButton('Выйти в главное меню')
        markup.row(btnback)
        bot.send_message(message.chat.id, f'{message.from_user.first_name}, вы зашли в аккаунт "Сотрудника"!',
                         reply_markup=markup)
    else:
        bot.send_message(message.chat.id, f'{message.from_user.first_name}, для вас эта команда не доступна!')


# просто будет, потом если что удалю (доп инфа)
# @bot.message_handler()
# def on_click(message):
# if message.text == 'Перейти на сайт':
#     webbrowser.open('https://balkon-kld.ru')
# elif message.text == 'Прайс-лист компании':
#     bot.send_message(message.chat.id, '<b>Цена услуг:<b/>', parse_mode='html')
# elif message.text == 'Чем занимается компания':
#     bot.send_message(message.chat.id, '<b>Услуги:<b/>', parse_mode='html')

# @bot.message_handler(commands=['switch'])
# def switch(message):
#     markup = types.InlineKeyboardMarkup()
#     switch_button = types.InlineKeyboardButton(text='Try', switch_inline_query="@physicist_agr")
#     markup.add(switch_button)
#     bot.send_message(message.chat.id, "Выбрать чат", reply_markup=markup)


# @bot.message_handler(commands=['prost'])
# def start(message):
#     markup = types.InlineKeyboardMarkup()
#     buttonA = types.InlineKeyboardButton('A', callback_data='a')
#     buttonB = types.InlineKeyboardButton('B', callback_data='b')
#     buttonC = types.InlineKeyboardButton('C', callback_data='c')
#     markup.row(buttonA, buttonB)
#     markup.row(buttonC)
#     bot.send_message(message.chat.id, 'It works!', reply_markup=markup)

@bot.message_handler(commands=['help'])
def helping_(message):
    try:
        with open('help.txt', 'r', encoding='utf-8') as f:
            help_article = f.read()
            if not help_article:
                bot.send_message(message.chat.id, 'Произошел сбой!')
            else:
                bot.send_message(message.chat.id, help_article)
    except FileNotFoundError:
        bot.send_message(message.chat.id, 'Произошел сбой!')


@bot.message_handler(commands=['web', 'site'])
def site(message):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton('Pro Service Калининград', url='https://balkon-kld.ru')
    markup.add(button1)
    bot.send_message(message.chat.id, 'Нажми на кнопку и перейди на сайт', reply_markup=markup)
    webbrowser.open('https://balkon-kld.ru')


@bot.message_handler(commands=['portfolio'])
def site_portfolio(message):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton('Перейти для просмотра портфолио', url='https://www.balkon-kld.ru/portfolio/')
    markup.add(button1)
    bot.send_message(message.chat.id, 'Портфолио компании Pro Service Калининград', reply_markup=markup)


@bot.message_handler(commands=['support'])
def technical_support(message):
    keyboard = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton(text="Перейти в чат", url="https://web.telegram.org/a/#678729167")
    keyboard.add(url_button)
    img = open('img//support//woman.jpg', 'rb')
    text = 'Мы всегда готовы помочь вам решить любую проблему или ответить на любой вопрос.' \
           'Оставайтесь на связи с нами, и мы сделаем все возможное, чтобы обеспечить вам самый ' \
           'высокий уровень сервиса. Не стесняйтесь обращаться к нам с любыми вопросами или предложениями ' \
           '- ваше удовлетворение является нашим главным приоритетом.'
    bot.send_photo(message.chat.id, photo=img, caption=text, reply_markup=keyboard)


@bot.message_handler(commands=['id'])
def unique(message):
    bot.send_message(message.chat.id, f'ID: {message.from_user.id}')


# @bot.callback_query_handler(func=lambda call: call.data == 'unsubscribe')
# def callback_query_unsubscribe(call):
#     us_id = call.message.from_user.id
#     db_delete_sale(user_id=us_id)
#     bot.send_message(call.message.chat.id, 'Вы отписались!')
#     get_posts()


@bot.callback_query_handler(func=lambda call: call.data == 'unsubscribe')
def callback_query_unsubscribe(message):
    us_id = message.from_user.id
    db_delete_sale(user_id=us_id)
    # message_unsubscribe()
    get_posts()


# def message_unsubscribe(call):
#     bot.send_message(call.message.chat.id, 'Вы отписались!')


def db_delete_sale(user_id: str):
    cursor.execute('DELETE FROM MailingSale WHERE user_id = ?', (user_id,))
    conn.commit()
    get_posts()


@bot.message_handler(commands=['sale'])
def sale_mes(message):
    try:
        us_id = message.from_user.id
        us_name = message.from_user.first_name
        us_sname = message.from_user.last_name
        username = message.from_user.username
        db_table_sale(user_id=us_id, user_name=us_name, user_surname=us_sname, username=username)
        bot.send_message(message.chat.id, 'Поздравляю, теперь Вы участник наших акций!')
    except sqlite3.IntegrityError:
        keyboard = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(text='Отписаться от наших предлжений', callback_data='unsubscribe')
        keyboard.add(button)
        bot.send_message(message.chat.id, 'Вы уже участник наших акций!', reply_markup=keyboard)


def db_table_sale(user_id: int, user_name: str, user_surname: str, username: str):
    cursor.execute('INSERT INTO MailingSale (user_id, user_name, user_surname, username) VALUES (?, ?, ?, ?)',
                   (user_id, user_name, user_surname, username))
    conn.commit()


def send_multiple_photos(message):
    text = 'Вот 10 наших сертификтов!' \
           'У нас их больше, хотите увидеть все переходите по ссылку! '
    path_absolut = 'img//certificates'
    # Получаем список всех файлов в папке
    file_list = os.listdir(path_absolut)
    # Фильтруем список, оставляем только файлы с расширением .jpg или .png (или другими поддерживаемыми форматами)
    photo_list = [file for file in file_list if file.endswith('.jpg') or file.endswith('.png')]
    # Если в папке есть меньше 10 фотографий, выводим сообщение об этом
    if len(photo_list) < 10:
        print("В папке недостаточно фотографий!")
    else:
        # Рандомно выбираем 10 фотографий из списка
        selected_photos = random.sample(photo_list, 10)
    os.chdir('img//certificates')
    media = [InputMediaPhoto(media=open(photo, 'rb'), caption=text) for photo in selected_photos]
    bot.send_media_group(chat_id=message.chat.id, media=media)
    os.chdir('E:/PROGRAMM/BOT')


def find_demand(message):
    try:
        us_text = message.text
        user = cursor.execute(
            'select Contract.contact_number, Demand.FIO, Demand.address, Type_pay.Pay, Contract.sum, Executor.FIO, Status_work.status from Contract join Type_pay on Contract.id_type_pay = Type_pay.id join Status_work on Contract.id_status = Status_work.id join Demand on Contract.contact_number = Demand.contract_number join Executor on Executor.id = Demand.id_executor where Contract.contact_number == %d' % int(
                us_text)).fetchall()
        if user:
            contact = []
        message_text = []
        text = ''
        for per in user:
            contract_dict = {
                'Номер договора:': per[0],
                'ФИО заказщика:': per[1],
                'Адрес установки:': per[2],
                'Тип оплаты:': per[3],
                'Стоимость услуги:': per[4],
                'ФИО исполнителя:': per[5],
                'Статус заказа:': per[6],
            }
        contact.append(contract_dict)
        print(contract_dict)
        for key, value in contract_dict.items():
            message_text += (key, value)
        print(message_text)
        for item in message_text:
            text += f'{item}\n'
        bot.send_message(message.chat.id, text)
    except ValueError:
        markup = types.InlineKeyboardMarkup()
        btn_replay = types.InlineKeyboardButton('Попробовать ещё раз?', callback_data='replay')
        markup.add(btn_replay)
        bot.send_message(message.chat.id, 'Договор состоит имеет иолько числа, введити то их!', reply_markup=markup)
    except UnboundLocalError:
        markup = types.InlineKeyboardMarkup()
        btn_replay = types.InlineKeyboardButton('Попробовать ещё раз?', callback_data='replay')
        markup.add(btn_replay)
        bot.send_message(message.chat.id, 'Упс, такой заявки я не нашел!', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'replay')
def find_replay(call: types.CallbackQuery):
    bot.send_message(call.message.chat.id, 'Пробовать ещё раз!')





@bot.message_handler()
def info(message):
    if message.text.lower() == 'id':
        bot.reply_to(message, f'ID: {message.from_user.id}')
    elif message.text == 'Cайт Pro Service':
        site(message)
    elif message.text == 'О компании':
        markup = types.ReplyKeyboardMarkup()
        btnsite = types.KeyboardButton('Cайт Pro Service')
        markup.row(btnsite)
        btninf = types.KeyboardButton('Контактная информация компании')
        markup.row(btninf)
        btncmp = types.KeyboardButton('Чем занимается компания?')
        markup.row(btncmp)
        btnportfolio = types.KeyboardButton('Портфолио компании Pro Service Калининград')
        markup.row(btnportfolio)
        btncertificates = types.KeyboardButton('Наши сертификаты')
        markup.row(btncertificates)
        btnback = types.KeyboardButton('Выйти в главное меню')
        markup.row(btnback)
        bot.send_message(message.chat.id, 'Информация о компании:', reply_markup=markup)
    elif message.text == 'Прайс-лист компании 🗒':
        prc_list = cursor.execute('SELECT service, price FROM PriceList').fetchall()
        message_text = ''
        for res in prc_list:
            message_text += '{0} - {1} руб.\n'.format(res[0], res[1])
        bot.send_message(message.chat.id, 'Стоимость услуг:\n' + message_text + '\n Цена указанна за один м2')
    elif message.text == 'Быть в курсе акцуий 🚨':
        sale_mes(message)
    elif message.text == 'Cайт Pro Service':
        site(message)
    elif message.text == 'Связь с оператором':
        technical_support(message)
    elif message.text == 'Чем занимается компания?':
        try:
            with open('company.txt', 'r', encoding='utf-8') as f:
                company_article = f.read()
                if not company_article:
                    bot.send_message(message.chat.id, 'Произошел сбой!')
                else:
                    bot.send_message(message.chat.id, company_article)
        except FileNotFoundError:
            bot.send_message(message.chat.id, 'Произошел сбой!')
    elif message.text == 'Контактная информация компании':
        try:
            with open('info.txt', 'r', encoding='utf-8') as f:
                info_article = f.read()
                if not info_article:
                    bot.send_message(message.chat.id, 'Произошел сбой!')
                else:
                    bot.send_message(message.chat.id, info_article)
        except FileNotFoundError:
            bot.send_message(message.chat.id, 'Произошел сбой!')
    elif message.text == 'Выйти в главное меню':
        markup = types.ReplyKeyboardMarkup()
        btnsite = types.KeyboardButton('О компании')
        markup.row(btnsite)
        btnprs = types.KeyboardButton('Прайс-лист компании 🗒')
        markup.row(btnprs)
        btnstatus = types.KeyboardButton('Статус заказа')
        markup.row(btnstatus)
        btnsrc = types.KeyboardButton('Быть в курсе акцуий 🚨')
        markup.row(btnsrc)
        btn_support = types.KeyboardButton('Связь с оператором')
        markup.row(btn_support)
        bot.send_message(message.chat.id, 'Вы вышли в главном меню', reply_markup=markup)
    elif message.text == 'Портфолио компании Pro Service Калининград':
        site_portfolio(message)
    elif message.text == 'Наши сертификаты':
        send_multiple_photos(message)
    elif message.text == 'Статус заказа' or message.text == 'Пробовать ещё раз':
        msg = bot.send_message(message.chat.id, 'Пожалуйства, введите номер договора.')
        bot.register_next_step_handler(msg, find_demand)





    else:
        bot.send_message(message.chat.id, 'I dont know!')


bot.polling(none_stop=True)

# # запускаем бота
# if __name__ == '__main__':
#     while True:
#         # в бесконечном цикле постоянно опрашиваем бота — есть ли новые сообщения
#         try:
#             bot.polling(none_stop=True, interval=0)
#         # если возникла ошибка — сообщаем про исключение и продолжаем работу
#         except Exception as e:
#             print('❌❌❌❌❌ Сработало исключение! ❌❌❌❌❌')
