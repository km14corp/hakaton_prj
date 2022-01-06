from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

b1 = InlineKeyboardButton('Режим Работы', callback_data='b1')
b2 = InlineKeyboardButton('Записаться', callback_data='b2')
kb1 = InlineKeyboardMarkup().add(b1).add(b2)

bk1 = InlineKeyboardButton('Первый корт', callback_data='bk1')
bk2 = InlineKeyboardButton('Второй корт', callback_data='bk2')
bk3 = InlineKeyboardButton('Третий корт', callback_data='bk3')
kb2 = InlineKeyboardMarkup().add(bk1).add(bk2).add(bk3)

bt1 = InlineKeyboardButton('Изяслав Ростиславович', callback_data='bt1')
bt2 = InlineKeyboardButton('Ибанат Магомедович', callback_data='bt2')
bt3 = InlineKeyboardButton('Елена Чмых', callback_data='bt3')
bt4 = InlineKeyboardButton('Отказаться от услуг тренера', callback_data='bt4')
kb3 = InlineKeyboardMarkup().add(bt1).add(bt2).add(bt3).add(bt4)

bi1 = InlineKeyboardButton('Да', callback_data='bi1')
bi2 = InlineKeyboardButton('Нет', callback_data='bi2')
kb4 = InlineKeyboardMarkup().add(bi1).add(bi2)
def make_markup(list_of_items):
    kb = InlineKeyboardMarkup()
    for i in list_of_items:
        button = InlineKeyboardButton(i, callback_data=i)
        kb.add(button)
    return kb