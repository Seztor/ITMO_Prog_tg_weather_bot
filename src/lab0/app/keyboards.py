from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from urllib3 import request

main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Выбрать локацию', callback_data='call_but1_weather')],
    [InlineKeyboardButton(text='О боте', callback_data='call_but2_about'),
     InlineKeyboardButton(text='Настройки', callback_data='call_but3_settings')]])


but_to_0 = InlineKeyboardButton(text='Назад ⤴', callback_data='call_back_to_0')

back_but_to_0 = InlineKeyboardMarkup(inline_keyboard=[[but_to_0]])



back_but_to_0_plus_settings = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Цельсий', callback_data='temptype_cels')],
                                                                    [InlineKeyboardButton(text='Фаренгейт', callback_data='temptype_far')],
                                                                    [InlineKeyboardButton(text='Кельвин', callback_data='temptype_kelv')],
                                                                    [but_to_0]])

but_location = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Ввести город', callback_data='call_type_city')],
    [InlineKeyboardButton(text='Ввести координаты', callback_data='call_but_type_cords')],
    [but_to_0]])


but_to_1 = InlineKeyboardButton(text='Назад ⤴', callback_data='call_back_to_1')

back_but_to_1 = InlineKeyboardMarkup(inline_keyboard=[[but_to_1]])

get_number = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отправить номер',
                                                           request_contact=True)]],resize_keyboard=True)