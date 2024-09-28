from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.filters import CommandStart, Command
from aiogram import F, Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from src.lab0.base_data.data_disp import update_user_data, get_users_data, check_user_data
import src.lab0.app.keyboards as kb
from src.lab0.weather_data_api.weather_data_visualer import get_visual_data_current_weather, \
    get_visual_data_few_days_weather
from src.lab0.weather_data_api.weather_disp import (get_city_by_coords, get_current_weather_by_cords, get_cords_by_city,
                                                    get_orig_city_name, get_few_days_weather_by_cords)

# from annotated_types.test_cases import cases

handler_router = Router()


#подгрузка фото
photo_about = FSInputFile('C:/Users/pavel/PycharmProjects/tg_bot/src/lab0/media/about.jpg')
photo_temp = FSInputFile('C:/Users/pavel/PycharmProjects/tg_bot/src/lab0/media/temperature.png')
photo_main = FSInputFile('C:/Users/pavel/PycharmProjects/tg_bot/src/lab0/media/main_photo.png')
photo_location = FSInputFile('C:/Users/pavel/PycharmProjects/tg_bot/src/lab0/media/location.png')
photo_city = FSInputFile('C:/Users/pavel/PycharmProjects/tg_bot/src/lab0/media/city.png')
photo_cords = FSInputFile('C:/Users/pavel/PycharmProjects/tg_bot/src/lab0/media/cords.png')
photo_forecast = FSInputFile('C:/Users/pavel/PycharmProjects/tg_bot/src/lab0/media/forecast.png')


#класс состояний
class Weather(StatesGroup):
    state_get_city = State()
    state_cords_pos = State()


#0 menu (Главное)
@handler_router.message(CommandStart())
async def main_menu(message: Message, state: FSMContext):
    await state.clear()
    check_user_data(message.from_user.id, message.from_user.first_name)
    await message.answer_photo(photo_main ,caption=f'🌏 Hello {message.from_user.first_name},'
                                                   f' this is a weather forecast bot!\n📝 Select menu item:',
                               reply_markup=kb.main)


@handler_router.callback_query(F.data == 'call_back_to_0')
async def main_menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    check_user_data(callback.from_user.id, callback.from_user.first_name)
    photo_main_inp = InputMediaPhoto(media=photo_main,
                                     caption=f'🌏 Hello {callback.from_user.first_name},'
                                             f' this is a weather forecast bot!\n📝 Select menu item:')
    await callback.message.edit_media(photo_main_inp, reply_markup=kb.main)




#Прогноз погоды
@handler_router.callback_query(F.data.in_(['call_but_weather','call_back_to_forecast']))
async def weather_forecast(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    check_user_data(callback.from_user.id, callback.from_user.first_name)
    if get_users_data(callback.from_user.id)['location'] != 'None':
        photo_forecast_inp = InputMediaPhoto(media=photo_forecast,
                                         caption=f'Select weather forecast date:')
        await callback.message.edit_media(photo_forecast_inp, reply_markup=kb.but_forecast)
    else:
        await callback.answer('Please select a location to\nget the weather forecast', show_alert=True)



#Прогноз на сегодня
@handler_router.callback_query(F.data == 'call_get_current_weather')
async def weather_forecast_current(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    if get_users_data(callback.from_user.id)['cords'] != 'Error cords':
        forecast_data_dict = get_current_weather_by_cords(*get_users_data(callback.from_user.id)['cords'].split(':'),
                                                          get_users_data(callback.from_user.id)['temptype'])
        #print(type(forecast_data_arr[0]),forecast_data_arr, 'forecast_data_arr')

        str_forecast_output = get_visual_data_current_weather(forecast_data_dict)
        photo_forecast_inp = InputMediaPhoto(media=photo_forecast,
                                         caption=f'Forecast in "{get_users_data(callback.from_user.id)['location']}" '
                                                 f'for today:\n{str_forecast_output}')
        await callback.message.edit_media(photo_forecast_inp, reply_markup=kb.back_but_to_forecast)
    else:
        await callback.answer("Coordinates is not defined")


#Прогноз на 5 дней
@handler_router.callback_query(F.data == 'call_get_few_days_weather')
async def weather_forecast_current(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    if get_users_data(callback.from_user.id)['cords'] != 'Error cords':
        forecast_data_list = get_few_days_weather_by_cords(*get_users_data(callback.from_user.id)['cords'].split(':'),
                                                          get_users_data(callback.from_user.id)['temptype'])
        # print(forecast_data_list)
        #print(type(forecast_data_arr[0]),forecast_data_arr, 'forecast_data_arr')

        str_forecast_output = get_visual_data_few_days_weather(forecast_data_list)
        photo_forecast_inp = InputMediaPhoto(media=photo_forecast,
                                         caption=f'Forecast in "{get_users_data(callback.from_user.id)['location']}" '
                                                 f'for 5 days:\n{str_forecast_output}')
        await callback.message.edit_media(photo_forecast_inp, reply_markup=kb.back_but_to_forecast)
    else:
        await callback.answer("Coordinates is not defined")





#установка роли
@handler_router.message(Command('setrole'))
async def role_man(message: Message):
    if str(message.from_user.id) == '902097397' or get_users_data(message.from_user.id)['role'] == 'admin':
        try:
            id_for_role, role = message.text.split(' ')[1:]
            if id_for_role.isdigit() and role in ('admin', 'user'):
                if get_users_data(int(id_for_role)):
                    update_user_data(role, int(id_for_role), 'role')
                    await message.answer(f'You changed role {get_users_data(int(id_for_role))['name']} to {role}')
                    await message.delete()
                else:
                    await message.answer('There is no user with this id')
            else:

                await message.answer('Invalid input')
        except:
            await message.answer('Invalid input')
    else:
        await message.answer('I don’t understand, write /start to begin')




#weather 1 menu (Выбрать локацию)
@handler_router.callback_query(F.data.in_(['call_but1_location','call_back_to_1']))
async def call_but2(callback: CallbackQuery, state: FSMContext):
    check_user_data(callback.from_user.id, callback.from_user.first_name)
    await state.clear()
    current_location = get_users_data(callback.from_user.id)['location']
    current_cords = get_users_data(callback.from_user.id)['cords']
    if current_location == 'None':
        current_location = 'not defined'
    if current_location == 'Error city':
        current_location = 'locality not found'
    if current_cords == 'None':
        current_cords = 'not defined'
    if current_cords == 'Error cords':
        current_cords = 'coordinates not found'
    photo_location_inp = InputMediaPhoto(media=photo_location, caption=f'Current location: {current_location}\n'
                                                                       f'Current coordinates: {current_cords}\n'
                                                                       f'Select location method:')
    await callback.message.edit_media(photo_location_inp, reply_markup=kb.but_location)




#Ввод города
@handler_router.callback_query(F.data == 'call_type_city')
async def call_type_city(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Weather.state_get_city)
    check_user_data(callback.from_user.id, callback.from_user.first_name)
    photo_city_inp = InputMediaPhoto(media=photo_city, caption=f'Enter the name of the locality\n'
                                                               f'point, and then go back:')
    await callback.message.edit_media(photo_city_inp, reply_markup=kb.back_but_to_1)


@handler_router.message(Weather.state_get_city)
async def type_city(message: Message, state: FSMContext):
    await state.update_data(city_name=message.text)
    data = await state.get_data()

    cords = get_cords_by_city(data['city_name'])
    orig_name = get_orig_city_name(data['city_name'])
    if cords == 'Error cords':
        update_user_data('Error city', message.from_user.id, 'location')
        update_user_data('Error cords', message.from_user.id, 'cords')
    else:
        if orig_name != 'Error city':
            update_user_data(orig_name, message.from_user.id, 'location')
        else:
            update_user_data(data['city_name'], message.from_user.id, 'location')
        update_user_data(cords, message.from_user.id, 'cords')
    await message.delete()




#Ввод координат
@handler_router.callback_query(F.data == 'call_but_type_cords')
async def call_type_cords(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Weather.state_cords_pos)
    check_user_data(callback.from_user.id, callback.from_user.first_name)
    photo_cords_inp = InputMediaPhoto(media=photo_cords, caption=f'Enter coordinates in "latitude:longitude"\n'
                                                                 f'format or submit a geolocation\n'
                                                                 f'and then return back')
    await callback.message.edit_media(photo_cords_inp, reply_markup=kb.back_but_to_1)


@handler_router.message(Weather.state_cords_pos)
async def type_cords(message: Message, state: FSMContext):
    if str(message.content_type) == 'ContentType.TEXT':
        #print('it is text')
        await state.update_data(cords_data=message.text)
        data = await state.get_data()
        try:
            lat, lon = data['cords_data'].strip().split(':')
            #print(get_city_by_coords(lat, lon))
            update_user_data(get_city_by_coords(lat, lon), message.from_user.id, 'location')
            update_user_data(f'{round(float(lat),5)}:{round(float(lon),5)}', message.from_user.id, 'cords')
        except:
            pass
        await message.delete()
    elif str(message.content_type) == 'ContentType.VENUE':
        #print('it is venue')
        await state.update_data(cords_data=message.venue)
        data = await state.get_data()
        print(data)
        dict_data = dict(list(data['cords_data'])[0][1])
        lat, lon = dict_data['latitude'], dict_data['longitude']
        #print(lat, lon)
        update_user_data(get_city_by_coords(lat, lon), message.from_user.id, 'location')
        update_user_data(f'{round(float(lat),5)}:{round(float(lon),5)}', message.from_user.id, 'cords')
        await message.delete()
    elif str(message.content_type) == 'ContentType.LOCATION':
        await state.update_data(cords_data=message.location)
        data = await state.get_data()
        dict_data = dict(data['cords_data'])
        lat, lon = dict_data['latitude'], dict_data['longitude']
        update_user_data(get_city_by_coords(lat, lon), message.from_user.id, 'location')
        update_user_data(f'{round(float(lat), 5)}:{round(float(lon), 5)}', message.from_user.id, 'cords')
        await message.delete()
    else:
        await message.delete()




#about 3 menu (О боте)
@handler_router.callback_query(F.data == 'call_but2_about')
async def call_but3(callback: CallbackQuery, state: FSMContext):
    check_user_data(callback.from_user.id, callback.from_user.first_name)
    await state.clear()
    photo_about_inp = InputMediaPhoto(media=photo_about,
                                      caption='Weather bot\n'
                                              'Creared by @Seztor\n'
                                              'Pavel Govorov')
    await callback.message.edit_media(photo_about_inp, reply_markup=kb.back_but_to_0)




#about 4 menu (Настройки температуры)
convert_temp_to_eng = {
    'cels': 'Celsius',
    'far': 'Fahrenheit',
    'kelv': 'Kelvin'
}

@handler_router.callback_query(F.data == 'call_but3_settings')
async def call_but4(callback: CallbackQuery, state: FSMContext):
    check_user_data(callback.from_user.id, callback.from_user.first_name)
    await state.clear()
    temptype = get_users_data(callback.from_user.id)['temptype']
    photo_temp_inp = InputMediaPhoto(media=photo_temp,
                                     caption=f'🌡️ Choose what to measure your temperature in\n'
                                             f'Now the temperature scale: {convert_temp_to_eng[temptype]}')

    await callback.message.edit_media(photo_temp_inp, reply_markup=kb.back_but_to_0_plus_settings)


@handler_router.callback_query(F.data.startswith('temptype_'))
async def call_but5(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    data = str(callback.data.split('_')[-1])
    temptype = get_users_data(callback.from_user.id)['temptype']
    await callback.answer(f'You have selected a scale "{convert_temp_to_eng[data].strip()}"')
    if temptype != data:
        update_user_data(data, callback.from_user.id, 'temptype')
    try:
        photo_temp_inp = InputMediaPhoto(
            media=photo_temp,
            caption=f'🌡️ Choose what to measure your temperature in\n'
                    f'Now the temperature scale: {convert_temp_to_eng[data]}')
        await callback.message.edit_media(photo_temp_inp, reply_markup=kb.back_but_to_0_plus_settings)

    except:
        await callback.answer()


@handler_router.callback_query(F.data == 'pass')
async def weather_forecast_current(callback: CallbackQuery):
    await callback.answer('In development')

#trash sms
@handler_router.message()
async def trash(message: Message):
    check_user_data(message.from_user.id, message.from_user.first_name)
    await message.reply('I don’t understand, write /start to begin')

# @handler_router.message(Command('reg'))
# async def register(message: Message, state: FSMContext):
#     await state.set_state(Register.name)
#     await message.answer('Введите имя')
#
# @handler_router.message(Register.name)
# async def register_name(message: Message, state: FSMContext):
#     await state.update_data(name=message.text)
#     await state.set_state(Register.age)
#     await message.answer('Введите возраст')
#
# @handler_router.message(Register.age)
# async def register_age(message: Message, state: FSMContext):
#     await state.update_data(age=message.text)
#     await state.set_state(Register.number)
#     await message.answer('Введите число', reply_markup=kb.get_number)
#
# # @handler_router.message(Register.number, F.contact)
# @handler_router.message(Register.number)
# async def register_num(message: Message, state: FSMContext):
#     if message.content_type == 'contact':
#         await state.update_data(number=message.contact.phone_number)
#         data = await state.get_data()
#         await message.answer(f'Имя: {data['name']}\nВозраст: {data['age']}'
#                              f'\nТел.: {data['number']}')
#         await state.clear()
#     else:
#         await message.answer('Отправьте данные через кнопку')
