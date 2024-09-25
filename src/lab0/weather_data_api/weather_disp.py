import requests
import datetime as dt

BASE_URL = "https://pro.openweathermap.org/data/2.5/weather?"
BASE_URL_CORDS = "http://pro.openweathermap.org/geo/1.0/reverse?"
TOKEN = "d20cc1f559cfdeccf79419d8b4e95137"


def get_city_by_coords(lat, lon):
    url = f'{BASE_URL_CORDS}appid={TOKEN}&lat={lat}&lon={lon}'
    response_getcity = requests.get(url).json()
    #print(response_getcity)
    try:
        return response_getcity[0]['name']
    except:
        return 'Error city'

def get_weather_by_city_name(city_name):
    url = f'{BASE_URL}appid={TOKEN}&q={city_name}'
    try:
        response = requests.get(url).json()
        #print(response)
        w_coord_dict = response['coord']
        w_weather_dict = response['weather'][0]
        w_main_dict = response['main']
        w_wind_dict = response['wind']
        w_clouds = response['clouds']
        w_sunrise = f'{dt.datetime.fromtimestamp(int(response['sys']['sunrise']))} GMT+3'
        w_sunset = f'{dt.datetime.fromtimestamp(int(response['sys']['sunset']))} GMT+3'
        #print(w_sunrise, w_sunset)
    except:
        print('TIME OUT')

if __name__ == 'main':
    get_weather_by_city_name(get_city_by_coords(55.164440, 61.436844))

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


