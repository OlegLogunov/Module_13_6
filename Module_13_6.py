from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import asyncio

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
kb.insert(button)
kb.insert(button2)

kb_in = InlineKeyboardMarkup(resize_keyboard=True)
button_in = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data="calories")
button_in2 = InlineKeyboardButton(text='Формулы расчёта', callback_data="formulas")
kb_in.insert(button_in)
kb_in.insert(button_in2)

s = 0
@dp.message_handler(commands=["start"])
async def start(message):
    await message.answer("Привет! Я бот, помогающий твоему здоровью.", reply_markup=kb)


@dp.message_handler(text="Рассчитать")
async def  main_menu(message):
    await message.answer("Выберите опцию:", reply_markup=kb_in)


@dp.callback_query_handler(text="formulas")
async def  get_formulas(call):
    await call.message.answer("Формула Миффлина-Сан Жеора для мужчин: 10 х вес (кг) + 6,25 x рост (см)"
                              " – 5 х возраст (г) + 5")

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.callback_query_handler(text="calories")
async def set_age(call):
    await call.message.answer("Введите свой возраст:")
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(ag=message.text)
    await message.answer("Введите свой рост:")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(grow=message.text)
    await message.answer("Введите свой вес:")
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weig=message.text)
    data = await state.get_data()
    norma = int(10 * int(data['weig']) + 6.25 * int(data['grow']) - 5 * int(data['ag']) + 5)
    await message.answer(f"Ваша норма в сутки {norma} ккал")
    await state.finish()


#     для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
