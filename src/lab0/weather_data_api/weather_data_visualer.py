def get_visual_data_current_weather(data: dict):


    data['weather condition'] = data.pop('description')
    data['wind speed'] = data.pop('speed')
    data['wind degree'] = data.pop('deg')
    data['cloudiness'] = data.pop('all')

    data['humidity'] = f'{data['humidity']} %'
    data['cloudiness'] = f'{data['cloudiness']} %'
    data['wind speed'] = f'{data['wind speed']} {data['wind_speed_type']}'
    data['pressure'] = f'{data['pressure']} Pa'
    data['wind degree'] = f'{data['wind degree']}°'

    #print(data)

    str_data = ''
    for i in ['weather condition','temp','pressure','humidity','wind speed','wind degree','cloudiness','sunrise','sunset']:
        str_data += f'{i.capitalize()}: {data[i]}\n'
    return str_data

