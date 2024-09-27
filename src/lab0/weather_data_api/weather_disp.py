import requests
import datetime as dt

#шаблоны url
BASE_URL_CORDS = "http://pro.openweathermap.org/geo/1.0/reverse?"
BASE_URL_CITY= "http://pro.openweathermap.org/geo/1.0/direct?"
#BASE_URL_CURRENT_WEATHER_BY_CITY = "https://pro.openweathermap.org/data/2.5/weather?"
BASE_URL_CURRENT_WEATHER_BY_CORDS = "https://pro.openweathermap.org/data/2.5/weather?"

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

def get_current_weather_by_cords(lat: str, lon: str, temptype: str):
    url = f'{BASE_URL_CURRENT_WEATHER_BY_CORDS}appid={TOKEN}&lat={lat}&lon={lon}&units={convert_temp_url[temptype]}'
    try:
        response = requests.get(url).json()
        #print(response)
        w_coord_dict = response['coord']
        w_weather_dict = response['weather'][0]
        w_wind_speed_type = {}
        add_simv = ''
        match temptype:
            case "cels":
                add_simv = '°C'
                w_wind_speed_type = {'wind_speed_type': 'meter/sec'}
            case "far":
                add_simv = '℉'
                w_wind_speed_type = {'wind_speed_type': 'miles/hour'}
            case "kelv":
                add_simv = 'K'
                w_wind_speed_type = {'wind_speed_type': 'meter/sec'}

        w_main_dict = dict(response['main'])
        w_main_dict_keys = list(w_main_dict.keys())[:4]
        for j in w_main_dict_keys:
            w_main_dict[j] = f'{w_main_dict[j]} {add_simv}'
        #print(w_main_dict)

        w_wind_dict = response['wind']
        w_clouds = response['clouds']
        w_sunrise = {'sunrise':f'{str(dt.datetime.fromtimestamp(int(response['sys']['sunrise']))).split()[1]} GMT+3'}
        w_sunset = {'sunset':f'{str(dt.datetime.fromtimestamp(int(response['sys']['sunset']))).split()[1]} GMT+3'}
        weather_data_dict = w_weather_dict | w_main_dict | w_wind_dict | w_wind_speed_type | w_clouds | w_sunrise | w_sunset
        #print(weather_data_dict)
        return weather_data_dict
    except:
        print('Error data')

# def get_current_weather_by_cords(lat: str, lon: str):
#     url = f'{BASE_URL_CURRENT_WEATHER_BY_CORDS}appid={TOKEN}&lat={lat}&lon={lon}'
#     response = requests.get(url).json()
#     print(response)


# cityname = 'دهستان چوپانان'
#
# print(get_cords_by_city(cityname))
# print(get_city_by_coords('32.698', '51.668'))

# print(get_current_weather_by_cords('34','54'))
# print(get_city_by_coords('34','54'))

# print(url2)
# #55.164440, 61.436844

#
# print(response_getcity)
# print(response_getcity[0]['name'])
# city = response_getcity[0]['name']
# city = 'Челябинск'
# url = f'{BASE_URL}appid={TOKEN}&q={city}'
# try:
#     response = requests.get(url).json()
#     print(response)
#
#     w_coord_dict = response['coord']
#     w_weather_dict = response['weather'][0]
#     w_main_dict = response['main']
#     w_wind_dict = response['wind']
#     w_clouds = response['clouds']
#     w_sunrise = f'{dt.datetime.fromtimestamp(int(response['sys']['sunrise']))} GMT+3'
#     w_sunset = f'{dt.datetime.fromtimestamp(int(response['sys']['sunset']))} GMT+3'
#
#     print(w_sunrise, w_sunset)
# except:
#     print('TIME OUT')
