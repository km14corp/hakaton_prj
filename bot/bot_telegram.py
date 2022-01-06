from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import os


b1 = InlineKeyboardButton('Режим Работы', callback_data='b1')
kb1 = InlineKeyboardMarkup().add(b1)

class info(StatesGroup):
    name = State()
    date = State()
    time = State()
    cort = State()
    trainer = State()
    inventory = State()
    chek = State()
    oplata = State()

bot=Bot(token='5034918189:AAF6W5Brq9UOZggdCyQl5r7VV0FT5jx5N9g')
#bot=Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot, storage=MemoryStorage())


async def on_startup(_):
    print('Бот в сети')


@dp.message_handler(commands=['start','help'])
async def commands_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Здравствуй, давай запишемся в сквош-клуб')
        await message.delete()
    except:
        await message.reply('Общение с ботом через ЛС, напишите ему: \nhttps://t.me/СпортзальчикBot')


#@dp.message_handler(commands=['Режим_работы'])
#async def sportzal_open_command(message: types.Message):
#    await bot.send_message(message.from_user.id, 'Пн-Пт: 7:00-22:00, Сб,Вс: 8:00-21:00')


@dp.message_handler(commands=['Записаться'], state = None)
async def reservation(message: types.Message):
    await info.name.set()
    await message.answer('Начнем! \nВведите полное имя')


@dp.callback_query_handler(lambda c: c.data == 'b1')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Пн-Пт: 7:00-22:00, Сб,Вс: 8:00-21:00')


@dp.message_handler(state=info.name)
async def get_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await info.next()
    await message.reply('Выберите дату бронирования')


@dp.message_handler(state = info.date)
async def get_name(message: types.Message, state: FSMContext):
    await info.next()
    await message.answer('Выберите время бронирования')


@dp.message_handler(state = info.time)
async def get_name(message: types.Message, state: FSMContext):
    await info.next()
    await message.answer('Выберите корт')


@dp.message_handler(state = info.cort)
async def get_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['cort'] = message.text
    await info.next()
    await message.answer('Выберите тренера')


@dp.message_handler(state = info.trainer)
async def get_name(message: types.Message, state: FSMContext):
    await info.next()
    await message.answer('Нужен ли Вам инвентарь?')


@dp.message_handler(state = info.inventory)
async def get_name(message: types.Message, state: FSMContext):
    await info.next()
    await message.answer('Вот ваш чек')


@dp.message_handler(state = info.chek)
async def get_name(message: types.Message, state: FSMContext):
    await info.next()
    await message.answer('К оплате 100 грн')


@dp.message_handler(state = info.oplata)
async def get_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await message.answer(str(data))
    await message.answer('Поздравляю')
    await state.finish()










executor.start_polling(dp, skip_updates=True, on_startup=on_startup)