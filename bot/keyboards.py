from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from data_base.hakaton_db import data_base

db = data_base('../data_base/main_db.db')
b1 = InlineKeyboardButton('Режим Работы', callback_data='b1')
b2 = InlineKeyboardButton('Записаться', callback_data='b2')
kb1 = InlineKeyboardMarkup().add(b1).add(b2)



bi1 = InlineKeyboardButton('Да', callback_data='bi1')
bi2 = InlineKeyboardButton('Нет', callback_data='bi2')
kb4 = InlineKeyboardMarkup().add(bi1).add(bi2)
def make_markup(list_of_items):
    kb = InlineKeyboardMarkup()
    for i in list_of_items:
        button = InlineKeyboardButton(i, callback_data=i)
        kb.add(button)
    return kb
kb3 = make_markup(db.return_list_names('coach'))
bt = InlineKeyboardButton('Отказаться от услуг тренера', callback_data='bt1')
kb3.add(bt)
kb5 = make_markup(db.return_list_names('tools'))
kb6 = make_markup(['Да','Нет'])
kt = make_markup(['8:00', '9:00'])
