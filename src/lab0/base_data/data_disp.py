import json

file_path = "C:/Users/pavel/PycharmProjects/tg_bot/src/lab0/base_data/user_data.json"


#при наличии id возвращает данные по id, иначе все данные
def get_users_data(user_id: int | None = None):
    f = open(file_path, 'r')
    try:
        data_json = json.load(f)
        f.close()
        if user_id is None:
            return data_json
        else:
            return data_json[f'id{user_id}']
    except:
        return {}


#при наличии ключа обновляет данные по dict key, иначе все данные
def update_user_data(data: str | dict, user_id: int, key: str | None = None):
    data_json = get_users_data()
    f = open(file_path, 'w')
    if key is None:
        data_json[f'id{user_id}'] = data
    else:
        data_json[f'id{user_id}'][key] = data
    json.dump(data_json, f, indent=4, separators=(',', ': '))
    f.close()


#проверяет наличие данных о пользователе, иначе добавляет дефолт. данные
def check_user_data(user_id : int, name: str):
    f = open(file_path, 'r')
    default_data = {'name':str(name), 'temptype':'cels', 'location':'None', "cords": "None"}
    if str(user_id) == '902097397':
        default_data['role'] = 'admin'
    else:
        default_data['role'] = 'user'
    try:
        data_json = json.load(f)
        f.close()
        if data_json.get(f'id{user_id}'):
            pass
        else:
            update_user_data(default_data, user_id)
    except:
        update_user_data(default_data, user_id)
