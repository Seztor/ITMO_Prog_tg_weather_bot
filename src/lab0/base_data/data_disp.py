import json

file_path = "C:/Users/pavel/PycharmProjects/tg_bot/src/lab0/base_data/user_data.json"


#при наличии id возвращает данные по id, иначе все данные
def get_users_data(id=None):
    f = open(file_path, 'r')
    try:
        data_json = json.load(f)
        f.close()
        if id==None:
            return data_json
        else:
            return data_json[f'id{id}']
    except:
        return {}

#при наличии ключа обновляет данные по dict key, иначе все данные
def update_user_data(data, id, key=None):
    data_json = get_users_data()
    f = open(file_path, 'w')
    if key==None:
        data_json[f'id{id}'] = data
    else:
        data_json[f'id{id}'][key] = data
    json.dump(data_json, f, indent=4, ensure_ascii=False, separators=(',', ': '))
    f.close()

#проверяет наличие данных о пользователе, иначе добавляет дефолт. данные
def check_user_data(id, name):
    f = open(file_path, 'r')
    default_data = {'name':name, 'temptype':'cels', 'location':'None'}
    if str(id) == '902097397':
        default_data['role'] = 'admin'
    else:
        default_data['role'] = 'user'
    try:
        data_json = json.load(f)
        f.close()
        if data_json.get(f'id{id}'):
            pass
        else:
            update_user_data(default_data, id)
    except:
        update_user_data(default_data, id)


