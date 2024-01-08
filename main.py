import telebot
from currency_converter import CurrencyConverter
from telebot import types

bot = telebot.TeleBot('6442097585:AAEIkZXmd0R5uTMBmu3O3oaBLJCodFk_b8g')
currency = CurrencyConverter()
amount = 0

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    bot.send_message(user_id, 'Hi bro! Enter the count of money')
    bot.register_next_step_handler(message, summ)


def summ(message):
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'Unknown format! Please enter summ')
        bot.register_next_step_handler(message, summ)
        return

    if amount > 0:
        mark_up = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton(text='USD/EUR', callback_data='usd/eur')
        btn2 = types.InlineKeyboardButton(text='EUR/USD', callback_data='eur/usd')
        btn3 = types.InlineKeyboardButton(text='USD/GBP', callback_data='usd/gbp')
        btn4 = types.InlineKeyboardButton(text='GBP/USD', callback_data='gbp/usd')
        btn5 = types.InlineKeyboardButton(text='Another currency', callback_data='else')
        mark_up.add(btn1, btn2, btn3, btn4)
        mark_up.row(btn5)
        bot.send_message(message.chat.id, 'Choice second currency', reply_markup=mark_up)
    else:
        bot.send_message(message.chat.id, 'Summ must be more than 0! Please enter summ')
        bot.register_next_step_handler(message, summ)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data != 'else':
        values = call.data.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id, f'Result: {round(res, 2)}')
        bot.register_next_step_handler(call.message, summ)
    else:
        bot.send_message(call.message.chat.id, "Enter currency name by '/'! Like this USD/RUB!")
        bot.register_next_step_handler(call.message, my_currency)


def my_currency(message):
    try:
        values = message.text.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f'Result: {round(res, 2)}')
        bot.register_next_step_handler(message, summ)
    except Exception:
        bot.send_message(message.chat.id, 'Something goes wrong! ,Please resend currency')
        bot.register_next_step_handler(message, my_currency)


bot.polling(non_stop=True)