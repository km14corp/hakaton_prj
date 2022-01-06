from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.callback_data import CallbackData

from bot.States import info
from bot.config import TOKEN
from bot.keyboards import kb3, kb4, kb2, kb1
from simple_calendar import SimpleCalendar
import os

calendar_callback = CallbackData('simple_calendar', 'act', 'year', 'month', 'day')

bot = Bot(token=TOKEN)
# bot=Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot, storage=MemoryStorage())


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


@dp.callback_query_handler(calendar_callback.filter(), state=info.date)
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: dict, state: FSMContext):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        await callback_query.message.answer(
            f'Вы выбрали {date.strftime("%d/%m/%Y")}')
        async with state.proxy() as data:
            data['date'] = date.strftime("%d/%m/%Y")
    print(data['date'])
    await info.next()
    await bot.send_message(callback_query.from_user.id, 'Выберите время бронирования')


@dp.message_handler(state=info.time)
async def get_name(message: types.Message, state: FSMContext):
    await info.next()
    await message.answer('Выберите корт', reply_markup=kb2)


@dp.callback_query_handler(lambda c: c.data, state=info.cort)
async def cort(callback_query: types.CallbackQuery, state: FSMContext):
    code = callback_query.data[-1]
    if code == '1':
        async with state.proxy() as data:
            data['cort'] = 1
        await info.next()
        await bot.send_message(callback_query.from_user.id, 'Вы выбрали 1 корт \nВыберите тренера', reply_markup=kb3)
    elif code == '2':
        async with state.proxy() as data:
            data['cort'] = 2
        await info.next()
        await bot.send_message(callback_query.from_user.id, 'Вы выбрали 2 корт \nВыберите тренера', reply_markup=kb3)
    elif code == '3':
        async with state.proxy() as data:
            data['cort'] = 3
        await info.next()
        await bot.send_message(callback_query.from_user.id, 'Вы выбрали 3 корт \nВыберите тренера', reply_markup=kb3)


@dp.callback_query_handler(lambda c: c.data, state=info.coach)
async def cort(callback_query: types.CallbackQuery, state: FSMContext):
    code = callback_query.data[-1]
    if code == '1':
        async with state.proxy() as data:
            data['coach'] = 'Изяслав Ростиславович'
        await info.next()
        await bot.send_message(callback_query.from_user.id,
                               'Вы выбрали Изяслава Ростиславовича \nНужен ли вам инвентарь?', reply_markup=kb4)
    elif code == '2':
        async with state.proxy() as data:
            data['coach'] = 'Ибанат Магомедович'
        await info.next()
        await bot.send_message(callback_query.from_user.id, 'Вы выбрали Ибаната Магомедовича \nНужен ли вам инвентарь?',
                               reply_markup=kb4)
    elif code == '3':
        async with state.proxy() as data:
            data['coach'] = 'Елена Чмых'
        await info.next()
        await bot.send_message(callback_query.from_user.id, 'Вы выбрали Елену Чмых \nНужен ли вам инвентарь?',
                               reply_markup=kb4)
    elif code == '4':
        async with state.proxy() as data:
            data['coach'] = '-'
        await info.next()
        await bot.send_message(callback_query.from_user.id,
                               'Вы выбрали отказаться от услуг тренера \nНужен ли вам инвентарь?', reply_markup=kb4)


@dp.callback_query_handler(lambda c: c.data, state=info.inventory)
async def cort(callback_query: types.CallbackQuery, state: FSMContext):
    code = callback_query.data[-1]
    if code == '1':
        async with state.proxy() as data:
            data['inventory'] = 'Да'
        await info.next()
        await bot.send_message(callback_query.from_user.id, 'Вы выбрали приобрести инвентарь\n Предоставляю чек')
    elif code == '2':
        async with state.proxy() as data:
            data['inventory'] = 'Нет'
        await info.next()
        await bot.send_message(callback_query.from_user.id, 'Вы выбрали  не приобретать инвентарь\n Предоставляю чек')
    await bot.send_message(callback_query.from_user.id,
                           'ФИО: {}\nДата и время: {}\nКорт: {}\nТренер: {}\nИнвентарь: {}'.format(data['name'],
                                                                                                   data['date'],
                                                                                                   data['cort'],
                                                                                                   data['coach'],
                                                                                                   data['inventory']))
    await bot.send_message(callback_query.from_user.id, 'К оплате 100 грн')


@dp.message_handler(state=info.receipt)
async def get_name(message: types.Message, state: FSMContext):
    await message.answer('Плати налог')
    await state.finish()


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
