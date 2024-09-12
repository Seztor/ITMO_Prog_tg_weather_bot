import unittest
from src.lab1.calculator import calc

class CalculatorTestCase(unittest.TestCase):

    # Тест для проверки работы, можно удалить
    def test_one(self):
        self.assertEqual(1, 1)

    def test_addition(self):
        self.assertEqual(calc(1,2),3)