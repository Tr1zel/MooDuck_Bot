from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton


# btnBack = KeyboardButton('⏪Главное меню')
#--- Main Menu---
btn_inline1 = InlineKeyboardButton(text='TEXT', url='https://www.youtube.com/')
btnRandom = KeyboardButton('🎲Рандомное число')
btnInfo = KeyboardButton('ℹИнформация')
btnStick = KeyboardButton('Секретная кнопка🙃')
btnBack = KeyboardButton('⏪Главное меню')
btnRemind = KeyboardButton('🗓Напоминания')
#btnMain = KeyboardButton('Главное меню')
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnRandom, btnStick, btnRemind, btnInfo)


def btn_Main() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('Главное меню'))
    # kb.add(KeyboardButton())
    return kb

def get_cancel_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('/cancel'))
    return kb


#--Other MEnu---
# btnOther =  KeyboardButton('➡Другое')
# btnBack = KeyboardButton('⏪Главное меню')
# otherMenu = ReplyKeyboardMarkup(resize_keyboard= True).add(btnStick, btnBack)