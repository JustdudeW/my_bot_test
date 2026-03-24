import aiogram, aiohttp
import math
import os
import asyncio
import random
from datetime import datetime
from os import makedirs
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)

BOT_TOKEN = "TOKEN"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

counter = 0

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Привет"), KeyboardButton(text="Как дела")],
        [KeyboardButton(text="Пока"), KeyboardButton(text="Вопрос")]
    ],
    resize_keyboard=True
)

question_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Париж", callback_data="correct"),
            InlineKeyboardButton(text="Лондон", callback_data="wrong")
        ]
    ]
)

@dp.message(CommandStart())
async def start_handler(message: types.Message):
    name = message.from_user.full_name
    await message.answer(
        f"Salamaleikum, {name}!",
        reply_markup=main_kb
    )

@dp.message(F.text == "Привет")
async def hello_handler(message: types.Message):
    await message.answer("Привет, как дела?")

@dp.message(F.text == "Как дела")
async def how_are_you_handler(message: types.Message):
    await message.answer("У меня всё отлично")

@dp.message(F.text == "Пока")
async def bye_handler(message: types.Message):
    await message.answer("Пока! Удачи")

@dp.message(F.text == "Вопрос")
async def question_handler(message: types.Message):
    await message.answer(
        "Столица Франции?",
        reply_markup=question_kb
    )

@dp.callback_query(F.data.in_(["correct", "wrong"]))
async def answer_handler(callback: types.CallbackQuery):
    if callback.data == "correct":
        await callback.message.answer("Правильно!")
    else:
        await callback.message.answer("Неправильно!")

    await callback.answer()

@dp.message(Command("counter"))
async def counter_handler(message: types.Message):
    global counter

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="-", callback_data="minus"),
                InlineKeyboardButton(text="сброс", callback_data="reset"),
                InlineKeyboardButton(text="+", callback_data="plus"),
            ]
        ]
    )

    await message.answer(
        f"Счётчик: {counter}",
        reply_markup=kb
    )

@dp.callback_query(F.data.in_(["plus", "minus", "reset"]))
async def counter_buttons(callback: types.CallbackQuery):
    global counter

    if callback.data == "plus":
        counter += 1
    elif callback.data == "minus":
        counter -= 1
    elif callback.data == "reset":
        counter = 0

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="-", callback_data="minus"),
                InlineKeyboardButton(text="сброс", callback_data="reset"),
                InlineKeyboardButton(text="+", callback_data="plus"),
            ]
        ]
    )

    await callback.message.edit_text(
        f"Счётчик: {counter}",
        reply_markup=kb
    )

    await callback.answer()

@dp.message(Command("calc"))
async def calculator(message: types.Message, command: CommandObject):
    otvet = eval(command.args)
    await message.reply(f"Ваш ответ: {otvet}")

@dp.message(Command("bomboclat"))
async def bomboclat(message: types.Message, command: CommandObject):
    msg = " ".join(command.args.split()[:-1])
    count = int(command.args.split()[-1])
    await message.answer("БОМБОКЛАТ!!!")
    for _ in range(count):
        await message.answer(msg)

@dp.message(Command("pic"))
async def get_pic(message: types.Message):
    photo = types.FSInputFile("images.jpg")
    await message.reply_photo(photo=photo, caption="SIX-SEVEN :0")

@dp.message(Command("url_pic"))
async def get_url_pic(message:types.Message):
    url = "https://i.ytimg.com/vi/Wl7aACsdoaM/maxresdefault.jpg"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                img = await response.read()
                photo = types.BufferedInputFile(file=img, filename="img.jpg")
                await message.answer_photo(photo=photo, caption="Фото из интерната")
            else:
                await message.answer("Не удалось получить картинку")

@dp.message(F.sticker)
async def sticker_handler(message: types.Message):
    await message.reply(f"О стикер! {message.sticker.emoji}")

@dp.message(Command("factorial"))
async def factorial_handler(message: types.Message, command: CommandObject):
    try:
        n = int(command.args)
        result = math.factorial(n)
        await message.answer(f"Факториал {n} = {result}")
    except:
        await message.answer("Введите целое неотрицательное число")

@dp.message(Command("kvadr"))
async def kvadr_handler(message: types.Message, command: CommandObject):
    try:
        a, b, c = map(float, command.args.split())
        D = b ** 2 - 4 * a * c
        if D > 0:
            x1 = (-b + math.sqrt(D)) / (2 * a)
            x2 = (-b - math.sqrt(D)) / (2 * a)
            await message.answer(f"x1 = {x1}\nx2 = {x2}")
        elif D == 0:
            x = -b / (2 * a)
            await message.answer(f"x = {x}")
        else:
            await message.answer("Корней нет")
    except:
        await message.answer("Введите три числа: a b c")

@dp.message()
async def message_handler(message: types.Message):
    await message.reply("".join(reversed(message.text)))
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
