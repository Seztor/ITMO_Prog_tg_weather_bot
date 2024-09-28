import requests
import datetime as dt

#шаблоны url
BASE_URL_CORDS = "http://pro.openweathermap.org/geo/1.0/reverse?"
BASE_URL_CITY= "http://pro.openweathermap.org/geo/1.0/direct?"
BASE_URL_CURRENT_WEATHER_BY_CORDS = "https://pro.openweathermap.org/data/2.5/weather?"
BASE_URL_FEW_DAYS_WEATHER_BY_CORDS = "https://pro.openweathermap.org/data/2.5/forecast?"

TOKEN = open('C:/Users/pavel/PycharmProjects/tg_bot/src/lab0/tokens/TOKEN_API.txt').readline().strip()


def get_city_by_coords(lat: str, lon: str):
    url = f'{BASE_URL_CORDS}appid={TOKEN}&lat={lat}&lon={lon}'
    response_getcity = requests.get(url).json()
    #print(response_getcity)
    try:
        # print(response_getcity, 'response_getcity')
        return response_getcity[0]['name']
    except:
        return 'Error city'

def get_orig_city_name(city_name: str):
    url = f'{BASE_URL_CITY}appid={TOKEN}&q={city_name}'
    response = requests.get(url).json()
    try:
        return response[0]['name']
    except:
        return 'Error city'

def get_cords_by_city(city_name: str):
    url = f'{BASE_URL_CITY}appid={TOKEN}&q={city_name}'
    response = requests.get(url).json()
    try:
        cords = f'{round(response[0]['lat'],5)}:{round(response[0]['lon'],5)}'
        return cords
    except:
        return 'Error cords'


convert_temp_url = {
    'cels': 'metric',
    'far': 'imperial',
    'kelv': 'standard'
}

def get_add_symb_by_temptype(temptype: str):
    w_wind_speed_type = {}
    w_add_simv = {}
    match temptype:
        case "cels":
            w_add_simv = {'add_simv': '°C'}
            w_wind_speed_type = {'wind_speed_type': 'mt/s'}
        case "far":
            w_add_simv = {'add_simv': '℉'}
            w_wind_speed_type = {'wind_speed_type': 'ml/h'}
        case "kelv":
            w_add_simv = {'add_simv': 'K'}
            w_wind_speed_type = {'wind_speed_type': 'mt/s'}
    return w_add_simv | w_wind_speed_type

def get_current_weather_by_cords(lat: str, lon: str, temptype: str):
    url = f'{BASE_URL_CURRENT_WEATHER_BY_CORDS}appid={TOKEN}&lat={lat}&lon={lon}&units={convert_temp_url[temptype]}'
    try:
        response = requests.get(url).json()
        #print(response)
        #w_coord_dict = response['coord']
        w_weather_dict = response['weather'][0]

        w_add_symbols = get_add_symb_by_temptype(temptype)

        w_main_dict = response['main']
        w_wind_dict = response['wind']
        w_clouds = response['clouds']
        w_sunrise = {'sunrise':f'{str(dt.datetime.fromtimestamp(int(response['sys']['sunrise']))).split()[1]} GMT+3'}
        w_sunset = {'sunset':f'{str(dt.datetime.fromtimestamp(int(response['sys']['sunset']))).split()[1]} GMT+3'}
        weather_data_dict = w_weather_dict | w_main_dict | w_add_symbols | w_wind_dict  | w_clouds | w_sunrise | w_sunset
        #print(weather_data_dict)
        return weather_data_dict
    except:
        print('Error data')

def get_few_days_weather_by_cords(lat: str, lon: str, temptype: str):
    url = f'{BASE_URL_FEW_DAYS_WEATHER_BY_CORDS}appid={TOKEN}&lat={lat}&lon={lon}&units={convert_temp_url[temptype]}'
    try:
        response = requests.get(url).json()
        weather_data_list = []
        for dict_item in response['list']:
            w_weather_dict = dict_item['weather'][0]
            w_add_symbols = get_add_symb_by_temptype(temptype)
            w_main_dict = dict_item['main']
            w_wind_dict = dict_item['wind']
            w_time = {'dt': f'{str(dt.datetime.fromtimestamp(dict_item['dt']))[5:-3]} GMT+3'}
            weather_data_list.append(w_weather_dict | w_add_symbols | w_main_dict | w_wind_dict | w_time)
        # for i in weather_data_list:
        #     print(i)
        #     print('#############################################')
        return weather_data_list
    except:
        print('Error data')


get_few_days_weather_by_cords('55.164440','61.436844', 'cels')