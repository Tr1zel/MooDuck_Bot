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


list_of_stick = ('CAACAgIAAxkBAAEGuWJjkLtcWEB11Dlm2HaIXpMT28obAwACkBUAArTlyUvP28AHDr-D6SsE',
                 'CAACAgIAAxkBAAEGuWBjkLtVabpDWiwENj9dhCA_ua4JjgAC_hYAAhSpyEuADLjmWSoaqysE',
                 'CAACAgIAAxkBAAEGuVxjkLtQYsDvholaFmzjZDr8LVh1OAACiRUAAtI30Uvvk9YteS5JbCsE',
                 'CAACAgIAAxkBAAEGuVljkLtKwr4eQstcJrIB81LLLfMHMAACXxMAAi5eyEvZq78wYISWMysE',
                 'CAACAgIAAxkBAAEGuVhjkLtJqG45uAq5iWwlnG1_C0CNTwACzRMAAl6zyEvD5PzG428z7ysE',
                 'CAACAgIAAxkBAAEGuWxjkLvVlueF4Cps2bP_gAW1SuzfBwACuBMAAgZ_8EsdPfG8O_wkPisE')


storage = MemoryStorage
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage = MemoryStorage())


class ReminderStates(StatesGroup):
    textRemind = State()
    timeRemind = State()





@dp.message_handler(commands=['cancel'], state='*')
async def cmd_cancel(message: types.Message, state: FSMContext):
    if state is None:
        return
    await state.finish()
    await bot.send_message(chat_id=message.from_user.id,
                           text='Вы прервали создание напоминания! Если хотите продолжить начните заново.',
                           reply_markup=nav.mainMenu)

@dp.message_handler(lambda msg: msg.text == '🗓Напоминания')
async def text_create(message: types.Message) -> None:
    await message.reply('Давай создадим напоминание! Что бы начать напиши свой текст!',
                        reply_markup=nav.get_cancel_kb())
    await ReminderStates.textRemind.set()  # Установили текст напоминания

@dp.message_handler(state=ReminderStates.textRemind)
async def load_name(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['remind'] = message.text

    await message.reply('Через сколько минут тебе напомнить? ')
    await ReminderStates.next() # Поменяли состояние уже с фото и именем

@dp.message_handler(state=ReminderStates.timeRemind)
async def load_age(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['timeRemind'] = message.text
        await message.answer('Готово, Ваше напоминание успешно создано!')
        await bot.send_message(chat_id=message.from_user.id,
                               text=f'Ваше напоминание - {data["remind"]}.\nВремя через которое надо напомнить - {data["timeRemind"]} минут.',
                               reply_markup=nav.mainMenu)
    await state.finish()






@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_full_name = message.from_user.full_name
    await message.reply(f"Привет, {user_full_name}!", reply_markup = nav.mainMenu)

# Inline BUTTON
urlkb = InlineKeyboardMarkup(row_width=2)
btn_inline1 = InlineKeyboardButton(text='VK', url='https://vk.com/w1lli21')
btn_inline2 = InlineKeyboardButton(text='GitHub', url='https://github.com/Tr1zel/MooDuck_Bot')
urlkb.add(btn_inline1, btn_inline2)

# вызов Inline клавиатуры
@dp.message_handler(commands=['links'])
async def url_commands(message: types.Message):
    await message.answer('Ссылочки: ', reply_markup=urlkb)



@dp.message_handler()
async def bot_message(message: types.Message):
    #await bot.send_message(message.from_id, message.text)
    if message.text == '🎲Рандомное число':
        await bot.send_message(message.from_id, 'Ваше число: ' + str(random.randint(0,9999)))
    elif message.text == '⏪Главное меню':
        await bot.send_message(message.from_id, '⏪Главное меню', reply_markup= nav.mainMenu)
    # elif message.text == '➡Другое':
    #     await bot.send_message(message.from_id, '➡Другое', reply_markup= nav.otherMenu)
    elif message.text == 'ℹИнформация':
        await bot.send_message(message.from_id, 'Этот бот создан лучшим человеком на свете')
    #elif message.text == '🗓Напоминания':
        # await message.reply('Давай создадим напоминание! Что бы начать напиши сюда текст!',
        #                     reply_markup=nav.get_cancel_kb())
        # await ReminderStates.textRemind.set()       # Установили Текст Напоминания

    elif message.text == 'Секретная кнопка🙃':
        await message.answer('Держи Cолнышко!😜')
        await bot.send_sticker(message.from_id, sticker=(random.choice(list_of_stick)))
    else:
        await message.reply('Неизвестная команда')




if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
