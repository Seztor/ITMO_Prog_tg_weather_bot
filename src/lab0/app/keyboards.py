from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


#Главное меню
main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Weather forecast', callback_data='call_but_weather')],
    [InlineKeyboardButton(text='Select location', callback_data='call_but1_location')],
    [InlineKeyboardButton(text='About the bot', callback_data='call_but2_about'),
     InlineKeyboardButton(text='Settings', callback_data='call_but3_settings')]])


#Кнопка назад
but_to_0 = InlineKeyboardButton(text='Back ⤴', callback_data='call_back_to_0')
back_but_to_0 = InlineKeyboardMarkup(inline_keyboard=[[but_to_0]])


#настройки темп
back_but_to_0_plus_settings = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Celsius', callback_data='temptype_cels')],
                                                                    [InlineKeyboardButton(text='Fahrenheit', callback_data='temptype_far')],
                                                                    [InlineKeyboardButton(text='Kelvin', callback_data='temptype_kelv')],
                                                                    [but_to_0]])


#Прогноз погоды
but_forecast = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Current', callback_data='call_get_current_weather')],
    [InlineKeyboardButton(text='For 3 days', callback_data='pass')],
    [InlineKeyboardButton(text='For 2 weeks', callback_data='pass')],
    [InlineKeyboardButton(text='For a month', callback_data='pass')],
    [but_to_0]])


#выбор ввода города
but_location = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Enter a locality', callback_data='call_type_city')],
    [InlineKeyboardButton(text='Enter coordinates', callback_data='call_but_type_cords')],
    [but_to_0]])


but_to_1 = InlineKeyboardButton(text='Back ⤴', callback_data='call_back_to_1')

back_but_to_1 = InlineKeyboardMarkup(inline_keyboard=[[but_to_1]])

# get_number = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отправить номер',
#                                                            request_contact=True)]],resize_keyboard=True)