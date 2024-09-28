from urllib3.util.util import to_str


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

    visual_arr = ['weather condition','temp','feels like','pressure','humidity','wind speed','wind degree','cloudiness','sunrise','sunset']
    add_simv_arr = ['',f' {data['add_simv']}',f' {data['add_simv']}',' Pa', ' %', f' {data['wind_speed_type']}','°',' %','','']
    weather_condition_emoji = emoji_by_w_id(data['id'], data['icon'])
    add_emoji_arr = [weather_condition_emoji, '🌡️', '🌞', '♎', '💧', '💨', '🧭', '☁️','🌅','🌄']

    str_data = ''
    for i in range(len(visual_arr)):
        str_data += f'{add_emoji_arr[i]} {visual_arr[i].capitalize()}: {data[visual_arr[i]]}{add_simv_arr[i]}\n'
    return str_data


#прогноз (на 5 дней)
def get_visual_data_few_days_weather(data_list: list):\

    visual_arr = ['date','weather condition', 'temp', 'feels like', 'humidity', 'wind speed']
    str_data = '\n'
    # print(len(data_list))
    for dict_item in data_list:
        dict_item['weather condition'] = dict_item.pop('description')
        dict_item['feels like'] = dict_item.pop('feels_like')
        dict_item['wind speed'] = dict_item.pop('speed')
        dict_item['date'] = dict_item.pop('dt')
        weather_condition_emoji = emoji_by_w_id(dict_item['id'], dict_item['icon'])
        add_emoji_arr = ['🗓️', weather_condition_emoji, '🌡️', '🌞', '💧', '💨']
        add_simv_arr = ['', '', f' {dict_item['add_simv']}', f' {dict_item['add_simv']}', ' %',f' {dict_item['wind_speed_type']}']
        if len(str(dict_item['weather condition'])) > 25:
            dict_item['weather condition'] = str(dict_item['weather condition']).replace('light ','').replace('heavy ','')
        if '09:00' in dict_item['date'] or '15:00' in dict_item['date'] or '21:00' in dict_item['date']: # or
            date_arr = str(dict_item['date']).split()
            if '09:00' in dict_item['date']:
                str_data += f'🗓️ {date_arr[0]}\n'
            str_data += f'{date_arr[1]}: {weather_condition_emoji}{str(dict_item['weather condition'])}; 🌡️{round(dict_item['temp'],1)}{dict_item['add_simv']} ({round(dict_item['feels like'],1)}); 💨{dict_item['wind speed']}{dict_item['wind_speed_type']}\n'
            if '21:00' in dict_item['date']:
                str_data += '\n'




            # for i in range(len(visual_arr)):
            #     t_str_data += f'{add_emoji_arr[i]} {visual_arr[i].capitalize()}: {dict_item[visual_arr[i]]}{add_simv_arr[i]} '
            #     if i % 2 == 1 or i == 0:
            #         t_str_data += '\n'



    return str_data







