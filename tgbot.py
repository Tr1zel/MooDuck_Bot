import time
import logging
import os
from aiogram import Bot, Dispatcher, executor,types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import markups as nav
import random

TOKEN = "1230365437:AAHUmihZzRCdsRcypjmmWUrBNDFzlHtRzmg"

storage = MemoryStorage
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage = MemoryStorage())



class ProfileStatesGroup(StatesGroup):
    photo = State()
    name = State()
    age = State()
    desc = State()

@dp.message_handler(commands=['cancel'], state='*')
async def cmd_cancel(message: types.Message, state: FSMContext):
    if state is None:
        return
    await state.finish()
    await message.reply('Вы прервали создание анкеты! Если хотите продолжить начните заново.', reply_markup=nav.get_kb())



@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_full_name = message.from_user.full_name
    await message.reply(f"Привет, {user_full_name}!", reply_markup = nav.mainMenu)



#inline BUTTON
urlkb = InlineKeyboardMarkup(row_width=2)
btn_inline1 = InlineKeyboardButton(text='youtube', url='https://www.youtube.com/')
btn_inline2 = InlineKeyboardButton(text='Blue tracktor', url='https://www.youtube.com/watch?v=PhrBRUju2XE')
urlkb.add(btn_inline1, btn_inline2)

@dp.message_handler(commands=['ссылочки'])
async def url_commands(message: types.Message):
    await message.answer('Ссылочки: ', reply_markup=urlkb)


@dp.message_handler(commands=['create'])
async def cmd_create(message: types.Message) -> None:
    await message.reply('Давай изменим твой профиль! Что бы начать скинь свою фотографию!',
                        reply_markup=nav.get_cancel_kb())
    await ProfileStatesGroup.photo.set()  # Установили фото профиля

@dp.message_handler(lambda message: not message.photo, state=ProfileStatesGroup.photo)
async def check_photo(message: types.Message):      # проверка отправили ли фото
    await message.reply('Это не фотография!') #проверка на фото профиля



@dp.message_handler(content_types=['photo'], state=ProfileStatesGroup.photo)
async def load_photo(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id

    await message.reply('Теперь назови свое имя!')
    await ProfileStatesGroup.next() # Поменяли состояние уже с фото

@dp.message_handler(lambda message: not message.text.isdigit() or float(message.text) > 100, state=ProfileStatesGroup.age)
async def check_photo(message: types.Message):      # проверка текст является числом
    await message.reply('Введите реальный возраст!')  # Проверка на возраст(является ли числом и не больше 100)

@dp.message_handler(state=ProfileStatesGroup.name)
async def load_name(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['name'] = message.text

    await message.reply('Cколько тебе лет? ')
    await ProfileStatesGroup.next() # Поменяли состояние уже с фото и именем


@dp.message_handler(state=ProfileStatesGroup.age)
async def load_age(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['age'] = message.text

    await message.reply('А теперь расскажи о себе!')
    await ProfileStatesGroup.next()



@dp.message_handler(state=ProfileStatesGroup.desc)
async def load_desc(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['desc'] = message.text
        await message.answer('Готово, ваша анкета успешно создана!')
        await bot.send_photo(chat_id=message.from_user.id,
                             photo=data['photo'],
                             caption=f"{data['name']}, {data['age']}\n{data['desc']}")
    await state.finish()





@dp.message_handler()
async def bot_message(message: types.Message):
    #await bot.send_message(message.from_id, message.text)
    if message.text == '🎲Рандомное число':
        await bot.send_message(message.from_id, 'Ваше число: ' + str(random.randint(0,9999)))
    elif message.text == '⏪Главное меню':
        await bot.send_message(message.from_id, '⏪Главное меню', reply_markup= nav.mainMenu)
    elif message.text == '➡Другое':
        await bot.send_message(message.from_id, '➡Другое', reply_markup= nav.otherMenu)
    elif message.text == 'ℹИнформация':
        await bot.send_message(message.from_id, 'Этот бот создан лучшим человеком на свете')
    elif message.text == '🗓Напоминания':
        await bot.send_message(message.from_id, 'Допиливается🥰')
    elif message.text == 'Секретная кнопка🙃':
        await message.answer('Держи Мразь!')
        await bot.send_sticker(message.from_id, sticker='CAACAgIAAxkBAAEGqbdjizWjPJb7wiNzJwQoq3wAAV5zAicAAjkBAAKgMB835pn0RKG2LWIrBA')
    else:
        await message.reply('Неизвестная команда')




if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)