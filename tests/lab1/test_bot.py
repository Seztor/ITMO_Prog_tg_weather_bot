import unittest

from src.lab0.weather_data_api.weather_data_visualer import emoji_by_w_id
from src.lab0.weather_data_api.weather_disp import get_city_by_coords, get_cords_by_city, get_add_symb_by_temptype, \
    get_orig_city_name


class CalculatorTestCase(unittest.TestCase):

    # Тест для проверки работы, можно удалить
    def test(self):
        self.assertEqual(1, 1)

    def test_get_city_by_cords(self):
        self.assertEqual(get_city_by_coords('55.154', '61.4291'), 'Chelyabinsk')

    def test2_get_city_by_cords(self):
        self.assertEqual(get_city_by_coords('1.0', '1.0'), 'Error city')

    def test_get_cords_by_city(self):
        self.assertEqual(get_cords_by_city('Мадрид'), '40.4167:-3.70358')

    def test2_get_cords_by_city(self):
        self.assertEqual(get_cords_by_city('Подъегорьевск'), 'Error cords')

    def test_added_symbol(self):
        self.assertEqual(get_add_symb_by_temptype('cels'), {'add_simv': '°C', 'wind_speed_type': 'mt/s'})

    def test_get_orig_city_name(self):
        self.assertEqual(get_orig_city_name('владивосток'), 'Vladivostok')

    def get_emoji_by_w_id(self):
        self.assertEqual(emoji_by_w_id(800,'01d'),'☀️')

    def get_emoji_by_w_id2(self):
        self.assertEqual(emoji_by_w_id(800,'01d'),'☀️')

