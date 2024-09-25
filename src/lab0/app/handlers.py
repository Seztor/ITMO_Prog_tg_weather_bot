from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.filters import CommandStart, Command
from aiogram import F, Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from src.lab0.base_data.data_disp import update_user_data, get_users_data, check_user_data

import src.lab0.app.keyboards as kb
from annotated_types.test_cases import cases

handler_router = Router()



photo_about = FSInputFile('C:/Users/pavel/PycharmProjects/tg_bot/src/lab0/media/about.jpg')
photo_temp = FSInputFile('C:/Users/pavel/PycharmProjects/tg_bot/src/lab0/media/temperature.png')
photo_main = FSInputFile('C:/Users/pavel/PycharmProjects/tg_bot/src/lab0/media/main_photo.png')

# class Register(StatesGroup):
#     name = State()
#     age = State()
#     number = State()


#about 0 menu (Главное)
@handler_router.message(CommandStart())
async def main_menu(message: Message):
    check_user_data(message.from_user.id, message.from_user.first_name)
    await message.answer_photo(photo_main ,caption=f'🌏 Привет {message.from_user.first_name}, это бот прогноза погоды!\n📝 Выберите пункт меню:',
                         reply_markup=kb.main)


@handler_router.callback_query(F.data == 'call_back_to_0')
async def main_menu(callback: CallbackQuery):
    photo_main_inp = InputMediaPhoto(media=FSInputFile('C:/Users/pavel/PycharmProjects/tg_bot/src/lab0/media/main_photo.png'),
                                     caption=f'🌏 Привет {callback.from_user.first_name}, это бот прогноза погоды!\n📝 Выберите пункт меню:')
    await callback.message.edit_media(photo_main_inp, reply_markup=kb.main)


#установка роли
@handler_router.message(Command('setrole'))
async def main_menu(message: Message):
    if str(message.from_user.id) == '902097397' or get_users_data(message.from_user.id)['role'] == 'admin':
        try:
            id_for_role, role = message.text.split(' ')[1:]
            if id_for_role.isdigit() and role in ('admin', 'user'):
                if get_users_data(id_for_role):
                    update_user_data(role, id_for_role, 'role')
                    await message.answer(f'Вы поменяли роль {get_users_data(id_for_role)['name']} на {role}')
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


@handler_router.callback_query(F.data == 'call_but1_weather')
async def call_but2(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.answer('weather')


#about 3 menu (О боте)
@handler_router.callback_query(F.data == 'call_but2_about')
async def call_but3(callback: CallbackQuery):
    photo_about_inp = InputMediaPhoto(media=FSInputFile('C:/Users/pavel/PycharmProjects/tg_bot/src/lab0/media/about.jpg'),
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
    photo_temp_inp = InputMediaPhoto(media=FSInputFile('C:/Users/pavel/PycharmProjects/tg_bot/src/lab0/media/temperature.png'),
                                     caption=f'🌡️ Выберите в чем измерять температуру:'
                                             f'\nСейчас температурная шкала: {convert_temp_to_rus[temptype]}')

    await callback.message.edit_media(photo_temp_inp, reply_markup=kb.back_but_to_0_plus_settings)


@handler_router.callback_query(F.data.startswith('temptype_'))
async def call_but5(callback: CallbackQuery):
    data = str(callback.data.split('_')[-1])
    temptype = get_users_data(callback.from_user.id)['temptype']
    #await callback.answer(f'Вы выбрали шкалу "{convert_temp_to_rus[data]}"')
    if temptype != data:
        update_user_data(data, callback.from_user.id, 'temptype')
    try:
        photo_temp_inp = InputMediaPhoto(
            media=FSInputFile('C:/Users/pavel/PycharmProjects/tg_bot/src/lab0/media/temperature.png'),
            caption=f'🌡️ Выберите в чем измерять температуру:'
                    f'\nСейчас температурная шкала: {convert_temp_to_rus[data]}')
        await callback.message.edit_media(photo_temp_inp, reply_markup=kb.back_but_to_0_plus_settings)
        # await callback.message.edit_text(f'🌡️ Выберите в чем измерять температуру:'
        #                                                     f'\nСейчас температурная шкала: {convert_temp_to_rus[data]}',
        #                                 reply_markup=kb.back_but_to_0_plus_settings)

    except:
        await callback.answer()



#trash sms
@handler_router.message()
async def weather(message: Message):
    check_user_data(message.from_user.id, message.from_user.first_name)
    await message.answer('Не понял, напиши /start чтобы начать')

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
