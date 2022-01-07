from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.callback_data import CallbackData

from bot import keyboards
from excel_helper.excel_helper import court_number
from data_base.hakaton_db import data_base
from bot.States import info
from bot.config import TOKEN
from bot.keyboards import kb4, kb1, kb3, kb5, kb6, make_markup
from simple_calendar import SimpleCalendar
from excel_helper.excel_helper import Excel_helper

import os

db = data_base('../data_base/main_db.db')

calendar_callback = CallbackData('simple_calendar', 'act', 'year', 'month', 'day')

bot = Bot(token=TOKEN)
# bot=Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot, storage=MemoryStorage())
excel_db = Excel_helper('../excel_helper/qwerty')

async def on_startup(_):
    print('Бот в сети')


@dp.message_handler(commands=['start', 'help'])
async def commands_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Здравствуй, давай запишемся в сквош-клуб', reply_markup=kb1)
        await message.delete()
    except:
        await message.reply('Общение с ботом через ЛС, напишите ему: \nhttps://t.me/СпортзальчикBot')


@dp.callback_query_handler(lambda c: c.data == 'b1')
async def timetable(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Пн-Пт: 7:00-22:00, Сб,Вс: 8:00-21:00')


@dp.callback_query_handler(lambda c: c.data == 'b2', state=None)
async def booking(callback_query: types.CallbackQuery):
    await info.name.set()
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Начнем! \nВведите ФИО')


@dp.message_handler(state=info.name)
async def get_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await info.next()
    await message.answer("Выберите дату бронирования: ", reply_markup=await SimpleCalendar().start_calendar())

time = []
@dp.callback_query_handler(calendar_callback.filter(), state=info.date)
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: dict, state: FSMContext):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    global time
    if selected:
        await callback_query.message.answer(
            f'Вы выбрали {date.strftime("%d/%m/%Y")}')
        async with state.proxy() as data:
            data['date'] = date.strftime("%d.%m.%Y")
            print(data['date'])
    await info.next()
    time = excel_db.get_available_time(data['date'])
    await bot.send_message(callback_query.from_user.id, 'Выберите время бронирования', reply_markup=keyboards.make_markup(time))


@dp.callback_query_handler(lambda c: c.data, state=info.time)
async def cort(callback_query: types.CallbackQuery, state: FSMContext):
    global time
    code = callback_query.data
    print(code)
    for i in time:
        if code == i:
            async with state.proxy() as data:
                data['time'] = i
            kb2 = make_markup(excel_db.get_available_court(data['date'],data['time']))
            await info.next()
            await bot.send_message(callback_query.from_user.id,
                                   'Вы выбрали время - {} \nВыберите корт'.format(data['time']), reply_markup=kb2)


@dp.callback_query_handler(lambda c: c.data, state=info.cort)
async def cort(callback_query: types.CallbackQuery, state: FSMContext):
    code = callback_query.data
    print(code)
    for i in range(court_number+1):
        if code == str(i):
            async with state.proxy() as data:
                data['cort'] = i
            await info.next()
            await bot.send_message(callback_query.from_user.id, 'Вы выбрали {} корт \nВыберите тренера'.format(i),
                                   reply_markup=kb3)


@dp.callback_query_handler(lambda c: c.data, state=info.coach)
async def coach(callback_query: types.CallbackQuery, state: FSMContext):
    code = callback_query.data
    print(code)
    if code == db.return_list_names('coach')[0]:
        async with state.proxy() as data:
            data['coach'] = db.return_list_names('coach')[0]
        await info.next()
        await bot.send_message(callback_query.from_user.id,
                               'Вы выбрали {} \nНужен ли вам инвентарь?'.format(db.return_list_names('coach')[0]),
                               reply_markup=kb4)
    elif code == db.return_list_names('coach')[1]:
        async with state.proxy() as data:
            data['coach'] = db.return_list_names('coach')[1]
        await info.next()
        await bot.send_message(callback_query.from_user.id,
                               'Вы выбрали {} \nНужен ли вам инвентарь?'.format(db.return_list_names('coach')[1]),
                               reply_markup=kb4)
    elif code == db.return_list_names('coach')[2]:
        async with state.proxy() as data:
            data['coach'] = db.return_list_names('coach')[2]
        await info.next()
        await bot.send_message(callback_query.from_user.id,
                               'Вы выбрали {} \nНужен ли вам инвентарь?'.format(db.return_list_names('coach')[2]),
                               reply_markup=kb4)
    elif code == 'bt1':
        async with state.proxy() as data:
            data['coach'] = '-'
        await info.next()
        await bot.send_message(callback_query.from_user.id,
                               'Вы выбрали отказаться от услуг тренера \nНужен ли вам инвентарь?', reply_markup=kb4)


@dp.callback_query_handler(lambda c: c.data, state=info.inventory)
async def inventory(callback_query: types.CallbackQuery, state: FSMContext):
    code = callback_query.data[-1]
    if code == '1':
        async with state.proxy() as data:
            data['inventory'] = 'Да'
        await info.tools.set()
        await bot.send_message(callback_query.from_user.id,
                               'Вы выбрали приобрести инвентарь\n Что Вы бы хотели приобрести?', reply_markup=kb5)
    elif code == '2':
        async with state.proxy() as data:
            data['inventory'] = 'Нет'
            data['tools'] = ''
        await info.next()
        await bot.send_message(callback_query.from_user.id, 'Вы выбрали  не приобретать инвентарь\n Предоставляю чек')
        await bot.send_message(callback_query.from_user.id,
                               'ФИО: {}\nДата и время: {}, {time}\nКорт: {}\nТренер: {}\nИнвентарь: {}\n{}'.format(
                                   data['name'], data['date'], data['cort'], data['coach'], data['inventory'],
                                   data['tools'], time=data['time']))
        print(data)
        # full cost
        full_cost = 0
        full_cost += db.return_cost('coach', data['coach'])
        full_cost += db.return_time_cost('cost_weekdays', data['time'].split('-')[0])
        full_cost += sum(db.return_cost('tools', i) for i in data['tools'].split())
        await bot.send_message(callback_query.from_user.id, 'К оплате' + str(full_cost))
        if data['coach'] == '-':
            excel_db.set_property(data['date'], data['name'], data['time'], data['cort'])
        else:
            excel_db.set_property(data['date'], data['name'], data['time'], data['cort'], data['coach'])


@dp.callback_query_handler(lambda c: c.data, state=info.tools)
async def tools(callback_query: types.CallbackQuery, state: FSMContext):
    code = callback_query.data
    if code == db.return_list_names('tools')[0]:
        async with state.proxy() as data:
            data['tools'] = db.return_list_names('tools')[0]
        await info.choose.set()
        await bot.send_message(callback_query.from_user.id,
                               'Вы выбрали приобрести {}\n Приобрести еще {}?'.format(db.return_list_names('tools')[0],db.return_list_names('tools')[1]), reply_markup=kb6)
    elif code == db.return_list_names('tools')[1]:
        async with state.proxy() as data:
            data['tools'] = db.return_list_names('tools')[1]
        await info.choose_2.set()
        await bot.send_message(callback_query.from_user.id,
                               'Вы выбрали приобрести {}\n Приобрести еще {}?'.format(db.return_list_names('tools')[1],db.return_list_names('tools')[0]), reply_markup=kb6)


@dp.callback_query_handler(lambda c: c.data, state=info.choose)
async def choose(callback_query: types.CallbackQuery, state: FSMContext):
    code = callback_query.data
    if code == 'Да':
        async with state.proxy() as data:
            data['tools'] += ' ' + 'Ракетка'
        await info.receipt.set()
        await bot.send_message(callback_query.from_user.id, 'Вы выбрали добавить ракетку\nСоставляю чек')
        await bot.send_message(callback_query.from_user.id,
                               'ФИО: {}\nДата и время: {}\nКорт: {}\nТренер: {}\nИнвентарь: {}\n{}'.format(data['name'],
                                                                                                           data['date'],
                                                                                                           data['cort'],
                                                                                                           data[
                                                                                                               'coach'],
                                                                                                           data[
                                                                                                               'inventory'],
                                                                                                           data[
                                                                                                               'tools']))
        # full cost
        full_cost = 0
        full_cost += db.return_cost('coach', data['coach'])
        full_cost += db.return_time_cost('cost_weekdays', data['time'].split('-')[0])
        full_cost += sum(db.return_cost('tools', i) for i in data['tools'].split())
        print(full_cost)
        await bot.send_message(callback_query.from_user.id, 'К оплате ' + ' ' + str(full_cost))
        if data['coach'] == '-':
            Excel_helper.set_property(data['date'], data['name'], data['time'], data['cort'])
        else:
            Excel_helper.set_property(data['date'], data['name'], data['time'], data['cort'], data['coach'])
    else:
        async with state.proxy() as data:
            data['tools'] += ''
        await bot.send_message(callback_query.from_user.id, '\nСоставляю чек')
        await bot.send_message(callback_query.from_user.id,
                               'ФИО: {}\nДата и время: {}\nКорт: {}\nТренер: {}\nИнвентарь: {}\n{}'.format(data['name'],
                                                                                                           data['date'],
                                                                                                           data['cort'],
                                                                                                           data[
                                                                                                               'coach'],
                                                                                                           data[
                                                                                                               'inventory'],
                                                                                                           data[
                                                                                                               'tools']))
        # full cost
        full_cost = 0
        full_cost += db.return_cost('coach', data['coach'])
        full_cost += db.return_time_cost('cost_weekdays', data['time'].split('-')[0])
        full_cost += sum(db.return_cost('tools', i) for i in data['tools'].split())
        await bot.send_message(callback_query.from_user.id, 'К оплате ' + ' ' + str(full_cost))
        if data['coach'] == '-':
            excel_db.set_property(data['date'], data['name'], data['time'], data['cort'])
        else:
            excel_db.set_property(data['date'], data['name'], data['time'], data['cort'], data['coach'])

@dp.callback_query_handler(lambda c: c.data, state=info.choose_2)
async def choose_2(callback_query: types.CallbackQuery, state: FSMContext):
    code = callback_query.data
    if code == 'Да':
        async with state.proxy() as data:
            data['tools'] += ' ' + 'Мячик'
        await state.finish()
        await bot.send_message(callback_query.from_user.id, 'Вы выбрали добавить мячик\nСоставляю чек')
        await bot.send_message(callback_query.from_user.id,
                               'ФИО: {}\nДата и время: {}\nКорт: {}\nТренер: {}\nИнвентарь: {}\n{}'.format(data['name'],
                                                                                                           data['date'],
                                                                                                           data['cort'],
                                                                                                           data[
                                                                                                               'coach'],
                                                                                                           data[
                                                                                                               'inventory'],
                                                                                                           data[
                                                                                                               'tools']))
        # full cost
        full_cost = 0
        full_cost += db.return_cost('coach', data['coach'])
        full_cost += db.return_time_cost('cost_weekdays', data['time'].split('-')[0])
        full_cost += sum(db.return_cost('tools', i) for i in data['tools'].split())
        await bot.send_message(callback_query.from_user.id, 'К оплате ' +' '+str(full_cost))
        if data['coach'] == '-':
            excel_db.set_property(data['date'], data['name'], data['time'], data['cort'])
        else:
            excel_db.set_property(data['date'], data['name'], data['time'], data['cort'], data['coach'])
    else:
        async with state.proxy() as data:
            data['tools'] += ''
        await bot.send_message(callback_query.from_user.id, '\nСоставляю чек')
        await bot.send_message(callback_query.from_user.id,
                               'ФИО: {}\nДата и время: {}\nКорт: {}\nТренер: {}\nИнвентарь: {}\n{}'.format(data['name'],
                                                                                                           data['date'],
                                                                                                           data['cort'],
                                                                                                           data[
                                                                                                               'coach'],
                                                                                                           data[
                                                                                                               'inventory'],
                                                                                                           data[
                                                                                                               'tools']))
        # full cost
        full_cost = 0
        full_cost += db.return_cost('coach', data['coach'])
        full_cost += db.return_time_cost('cost_weekdays', data['time'].split('-')[0])
        full_cost += sum(db.return_cost('tools', i) for i in data['tools'].split())
        await bot.send_message(callback_query.from_user.id, 'К оплате ' + ' ' + str(full_cost))
        if data['coach'] == '-':
            excel_db.set_property(data['date'], data['name'], data['time'], data['cort'])
        else:
            excel_db.set_property(data['date'], data['name'], data['time'], data['cort'], data['coach'])




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
