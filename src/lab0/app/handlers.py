import asyncio
from logging import currentframe

from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.filters import CommandStart, Command
from aiogram import F, Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.methods.delete_message import DeleteMessage

from src.lab0.base_data.data_disp import update_user_data, get_users_data, check_user_data
import src.lab0.app.keyboards as kb
from src.lab0.weather_data_api.weather_disp import get_city_by_coords

# from annotated_types.test_cases import cases

handler_router = Router()



photo_about = FSInputFile('C:/Users/pavel/PycharmProjects/tg_bot/src/lab0/media/about.jpg')
photo_temp = FSInputFile('C:/Users/pavel/PycharmProjects/tg_bot/src/lab0/media/temperature.png')
photo_main = FSInputFile('C:/Users/pavel/PycharmProjects/tg_bot/src/lab0/media/main_photo.png')
photo_location = FSInputFile('C:/Users/pavel/PycharmProjects/tg_bot/src/lab0/media/location.png')
photo_city = FSInputFile('C:/Users/pavel/PycharmProjects/tg_bot/src/lab0/media/city.png')
photo_cords = FSInputFile('C:/Users/pavel/PycharmProjects/tg_bot/src/lab0/media/cords.png')

class Weather(StatesGroup):
    state_get_city = State()
    state_cords_pos = State()


#0 menu (Главное)
@handler_router.message(CommandStart())
async def main_menu(message: Message, state: FSMContext):
    await state.clear()
    check_user_data(message.from_user.id, message.from_user.first_name)
    await message.answer_photo(photo_main ,caption=f'🌏 Привет {message.from_user.first_name}, это бот прогноза погоды!\n📝 Выберите пункт меню:',
                         reply_markup=kb.main)


@handler_router.callback_query(F.data == 'call_back_to_0')
async def main_menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    photo_main_inp = InputMediaPhoto(media=FSInputFile('C:/Users/pavel/PycharmProjects/tg_bot/src/lab0/media/main_photo.png'),
                                     caption=f'🌏 Привет {callback.from_user.first_name}, это бот прогноза погоды!\n📝 Выберите пункт меню:')
    await callback.message.edit_media(photo_main_inp, reply_markup=kb.main)


#установка роли
@handler_router.message(Command('setrole'))
async def role_man(message: Message):
    if str(message.from_user.id) == '902097397' or get_users_data(message.from_user.id)['role'] == 'admin':
        try:
            id_for_role, role = message.text.split(' ')[1:]
            if id_for_role.isdigit() and role in ('admin', 'user'):
                if get_users_data(id_for_role):
                    update_user_data(role, id_for_role, 'role')
                    await message.answer(f'Вы поменяли роль {get_users_data(id_for_role)['name']} на {role}')
                    await message.delete()
                else:
                    await message.answer('Нет пользователя с таким id')
            else:

                await message.answer('Неверный ввод')
        except:
            await message.answer('Неверный ввод')
    else:
        await message.answer('Не понял, напиши /start чтобы начать')


# @handler_router.message(F.text == 'Погода')
# async def weather(message: Message):
#     await message.answer('Вот погода', reply_markup=kb.weather)


# @handler_router.callback_query(F.data == 'call_but1')
# async def call_but1(callback: CallbackQuery):
#     await callback.answer('')
#     await callback.message.answer('Вы выбрали погоду')





#weather 1 menu (Прогноз погоды)
@handler_router.callback_query(lambda F: F.data in ['call_but1_weather','call_back_to_1'])
async def call_but2(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    current_location = get_users_data(callback.from_user.id)['location']
    if current_location == 'None':
        current_location = 'не установлено'
    photo_location_inp = InputMediaPhoto(media=photo_location, caption=f'Текущее место: {current_location}\n'
                                                                       f'Выберите способ установления места:')
    await callback.message.edit_media(photo_location_inp, reply_markup=kb.but_location)



#Ввод города
@handler_router.callback_query(F.data == 'call_type_city')
async def call_type_city(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Weather.state_get_city)
    photo_city_inp = InputMediaPhoto(media=photo_city, caption=f'Введите название города\n'
                                                               f'и вернитесь назад:')
    await callback.message.edit_media(photo_city_inp, reply_markup=kb.back_but_to_1)


@handler_router.message(Weather.state_get_city)
async def type_city(message: Message, state: FSMContext):
    await state.update_data(city_name=message.text)
    data = await state.get_data()
    update_user_data(data['city_name'],message.from_user.id,'location')
    await message.delete()


#Ввод координат

@handler_router.callback_query(F.data == 'call_but_type_cords')
async def call_type_cords(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Weather.state_cords_pos)
    photo_cords_inp = InputMediaPhoto(media=photo_cords, caption=f'Введите координаты в формате "широта:долгота"\n'
                                                               f'или отправьте геопозицию\n'
                                                               f'и вернитесь назад:')
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
        except:
            pass
        await message.delete()
    elif str(message.content_type) == 'ContentType.VENUE':
        #print('it is venue')
        await state.update_data(cords_data=message.venue)
        data = await state.get_data()
        dict_data = dict(list(data['cords_data'])[0][1])
        lat, lon = dict_data['latitude'], dict_data['longitude']
        #print(lat, lon)
        update_user_data(get_city_by_coords(lat, lon), message.from_user.id, 'location')
        await message.delete()





#about 3 menu (О боте)
@handler_router.callback_query(F.data == 'call_but2_about')
async def call_but3(callback: CallbackQuery):
    photo_about_inp = InputMediaPhoto(media=photo_about,
                                      caption='Weather bot\n'
                                              'Creared by @Seztor\n'
                                              'Pavel Govorov')
    await callback.message.edit_media(photo_about_inp, reply_markup=kb.back_but_to_0)


#about 4 menu (Настройки)
convert_temp_to_rus = {
    'cels': '    Цельсий   ',
    'far': 'Фаренгейт',
    'kelv': '    Кельвин   '
}

@handler_router.callback_query(F.data == 'call_but3_settings')
async def call_but4(callback: CallbackQuery):
    temptype = get_users_data(callback.from_user.id)['temptype']
    photo_temp_inp = InputMediaPhoto(media=photo_temp,
                                     caption=f'🌡️ Выберите в чем измерять температуру:'
                                             f'\nСейчас температурная шкала: {convert_temp_to_rus[temptype]}')

    await callback.message.edit_media(photo_temp_inp, reply_markup=kb.back_but_to_0_plus_settings)


@handler_router.callback_query(F.data.startswith('temptype_'))
async def call_but5(callback: CallbackQuery):
    data = str(callback.data.split('_')[-1])
    temptype = get_users_data(callback.from_user.id)['temptype']
    await callback.answer(f'Вы выбрали шкалу "{convert_temp_to_rus[data].strip()}"')
    if temptype != data:
        update_user_data(data, callback.from_user.id, 'temptype')
    try:
        photo_temp_inp = InputMediaPhoto(
            media=photo_temp,
            caption=f'🌡️ Выберите в чем измерять температуру:'
                    f'\nСейчас температурная шкала: {convert_temp_to_rus[data]}')
        await callback.message.edit_media(photo_temp_inp, reply_markup=kb.back_but_to_0_plus_settings)

    except:
        await callback.answer()


#trash sms
@handler_router.message()
async def trash(message: Message):
    check_user_data(message.from_user.id, message.from_user.first_name)
    await message.reply('Не понял, напиши /start чтобы начать ' + str(message.content_type))

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
