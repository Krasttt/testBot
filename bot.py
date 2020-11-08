import cherrypy as cherrypy
import telebot
import config
from telebot import types

bot = telebot.TeleBot(config.TOKEN)


def create_menu_markup():
    markup = types.InlineKeyboardMarkup()
    button_1 = types.InlineKeyboardButton(f'{config.CARD} {config.BUTTON_1}', callback_data=config.BUTTON_1)
    button_2 = types.InlineKeyboardButton(f'{config.MONEY} {config.BUTTON_2}', callback_data=config.BUTTON_2)
    button_3 = types.InlineKeyboardButton(f'{config.CAR} {config.BUTTON_3}', callback_data=config.BUTTON_3)
    button_4 = types.InlineKeyboardButton(f'{config.ROBOT} {config.BUTTON_4}', callback_data=config.BUTTON_4)
    markup.row(button_1, button_2)
    markup.row(button_3, button_4)
    return markup


def create_markup():
    markup = types.InlineKeyboardMarkup()

    button_site = types.InlineKeyboardButton(f'{config.THUMBS_UP} Подтвердить', url='test.com', callback_data='site')
    button_menu = types.InlineKeyboardButton(f'{config.HOUSE} Вернуться к выбору продукта', callback_data='menu')
    markup.row(button_site)
    markup.row(button_menu)
    return markup


def create_markup_phone_number():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    button_accept = types.KeyboardButton(f'Предоставить', request_contact=True)
    button_deny = types.KeyboardButton('Отказаться')
    markup.row(button_accept)
    markup.row(button_deny)

    return markup


@bot.message_handler(commands=['start'])
def welcome(message):
    if message.from_user.first_name != '':
        name = f', {message.from_user.first_name}'
    else:
        name = ''
    bot.send_message(message.chat.id,
                     f'Добро пожаловать{name}!')
    bot.send_message(message.chat.id,
                     "Предоставьте номер телефона.",
                     reply_markup=create_markup_phone_number())


@bot.message_handler(content_types=['text'])
def chat(message):
    if message.chat.type == 'private':
        if message.text == 'Отказаться':
            bot.send_message(message.chat.id,
                             "Некоторые функции могут быть недоступны.",
                             reply_markup=types.ReplyKeyboardRemove())

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button = types.KeyboardButton(f'Предоставить номер телефона', request_contact=True)
            markup.add(button)

            bot.send_message(message.chat.id,
                             "Вы сможете предоставить номер телефона позже, нажав на кнопку ниже.",
                             reply_markup=markup)
        bot.send_message(message.chat.id,
                         'Выберите пункт из меню!',
                         reply_markup=create_menu_markup())


@bot.message_handler(content_types=['contact'])
def get_contact(message):
    bot.send_message(message.chat.id,
                     'Спасибо за понимание!',
                     reply_markup=types.ReplyKeyboardRemove())
    bot.send_message(message.chat.id,
                     'Выберите пункт из меню!',
                     reply_markup=create_menu_markup())


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'phone_number_accept':
                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text='Спасибо за понимание\nВыберите пункт из меню!',
                                      reply_markup=create_menu_markup())
                return

            elif call.data == 'phone_number_deny':
                bot.send_message(call.message.chat.id,
                                 'Печально\nВыберите пункт из меню!',
                                 reply_markup=create_menu_markup())
                return

            elif call.data == config.BUTTON_1:
                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text=f'{config.CARD} {config.BUTTON_1}',
                                      reply_markup=create_markup())
                return
            elif call.data == config.BUTTON_2:
                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text=f'{config.MONEY} {config.BUTTON_2}',
                                      reply_markup=create_markup())
                return
            elif call.data == config.BUTTON_3:
                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text=f'{config.CAR} {config.BUTTON_3}',
                                      reply_markup=create_markup())
                return
            elif call.data == config.BUTTON_4:
                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text=f'{config.ROBOT} {config.BUTTON_4}',
                                      reply_markup=create_markup())
            else:
                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text='Выберите новый пункт из меню',
                                      reply_markup=create_menu_markup())

    except Exception as e:
        print(repr(e))


bot.polling(none_stop=True)
