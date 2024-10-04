

def emoji_by_w_id(weather_id: int, icon: str):
    weather_condition_emoji = ''
    if 200 <= weather_id <= 232:
        weather_condition_emoji = '⛈️'
    elif 300 <= weather_id <= 321 or 520 <= weather_id <= 531:
        weather_condition_emoji = '🌧️'
    elif 500 <= weather_id <= 504:
        weather_condition_emoji = '🌦️'
    elif weather_id == 511 or 600 <= weather_id <= 622:
        weather_condition_emoji = '❄️'
    elif 700 <= weather_id <= 781:
        weather_condition_emoji = '🌫️'
    elif weather_id == 800:
        if 'd' in icon:
            weather_condition_emoji = '☀️'
        else:
            weather_condition_emoji = '🌙'
    elif weather_id == 801:
        weather_condition_emoji = '🌤️'
    elif weather_id == 802:
        weather_condition_emoji = '🌥️'
    elif 803 <= weather_id <= 804:
        weather_condition_emoji = '☁️'
    return weather_condition_emoji


#прогноз (сейчас)
def get_visual_data_current_weather(data: dict):
    data['weather condition'] = data.pop('description')
    data['wind speed'] = data.pop('speed')
    data['wind degree'] = data.pop('deg')
    data['cloudiness'] = data.pop('all')
    data['feels like'] = data.pop('feels_like')
    date_arr = str(data['dt']).split()
    normal_date = '.'.join(reversed(date_arr[0].split('-')))
    visual_arr = ['weather condition','temp','feels like','pressure','humidity','wind speed',
                  'wind degree','cloudiness','sunrise','sunset']
    add_simv_arr = ['',f" {data['add_simv']}", f" {data['add_simv']}",' hPa', ' %',
                    f" {data['wind_speed_type']}",'°',' %','','']
    weather_condition_emoji = emoji_by_w_id(data['id'], data['icon'])
    add_emoji_arr = [weather_condition_emoji, '🌡️', '🌞', '♎', '💧', '💨', '🧭', '☁️','🌅','🌄']

    str_data = ''
    for i in range(len(visual_arr)):
        if i == 0:
            str_data += (f"{add_emoji_arr[i]} <b>{visual_arr[i].capitalize()}</b>:"
                         f" <i>{data[visual_arr[i]]}</i>{add_simv_arr[i]}\n")
        else:
            str_data += (f"{add_emoji_arr[i]} <b>{visual_arr[i].capitalize()}</b>: "
                         f"{data[visual_arr[i]]}{add_simv_arr[i]}\n")

    return str_data, normal_date


#прогноз (на 5 дней)
def get_visual_data_few_days_weather(data_list: list):
    str_data = '\n'
    first_date = True
    for dict_item in data_list:
        weather_condition_emoji = emoji_by_w_id(dict_item['id'], dict_item['icon'])
        if len(str(dict_item['description'])) > 25:
            dict_item['description'] = (str(dict_item['description'])
                                        .replace('light ','')
                                        .replace('heavy ',''))
        if ('09:00' in dict_item['dt']
                or '15:00' in dict_item['dt']
                or '21:00' in dict_item['dt']): # or
            date_arr = str(dict_item['dt']).split()
            if '09:00' in dict_item['dt'] or (first_date and ('15:00' in dict_item['dt'] or '21:00' in dict_item['dt'])):
                normal_date = '.'.join(reversed(date_arr[0].split('-')))
                str_data += f"🗓️ <b>{normal_date}</b>\n"
                first_date = False
            str_data += (f"<b>{date_arr[1]}</b>: {weather_condition_emoji}<i>{str(dict_item['description'])}</i>;"
                         f" 🌡️{round(dict_item['temp'],1)}{dict_item['add_simv']}"
                         f" (<i>{round(dict_item['feels_like'],1)}</i>); 💨{dict_item['speed']}"
                         f"<i>{dict_item['wind_speed_type']}</i>\n")
            if '21:00' in dict_item['dt']:
                str_data += '\n'

    return str_data


def get_visual_data_two_weeks_weather(data_list: list):
    str_data = '\n'
    for i in range(len(data_list)):
        dict_item = data_list[i]
        weather_condition_emoji = emoji_by_w_id(dict_item['id'], dict_item['icon'])
        if len(str(dict_item['description'])) > 25:
            dict_item['description'] = (str(dict_item['description']).
                                        replace('light ','').
                                        replace('heavy ','').
                                        replace('with','w/'))
        date_arr = str(dict_item['dt']).split()
        normal_date = '.'.join(reversed(date_arr[0].split('-')))
        str_data += (f"🗓️<b>{normal_date}</b>: {weather_condition_emoji}<i>{str(dict_item['description'])}</i>;"
                     f" ☀️{round(dict_item['day'],1)}{dict_item['add_simv']}...🌙{round(dict_item['night'],1)}"
                     f"{dict_item['add_simv']}; 💨{dict_item['wind_speed']}{dict_item['wind_speed_type']}\n")
        if i == 6:
            str_data += '\n'
    return str_data


def get_visual_data_month_weather(data_list: list):
    str_data = '\n'
    for i in range(len(data_list)):
        dict_item = data_list[i]
        weather_condition_emoji = emoji_by_w_id(dict_item['id'], dict_item['icon'])
        date_arr = str(dict_item['dt']).split()
        normal_date = '.'.join(reversed(date_arr[0].split('-')))
        str_data += (f"🗓️<b>{normal_date}</b>: {weather_condition_emoji}{round(dict_item['day'],1)}"
                     f"{dict_item['add_simv']}; ").ljust(30,' ')
        if (i+1) % 2 == 0:
            str_data += '\n'
    return str_data





