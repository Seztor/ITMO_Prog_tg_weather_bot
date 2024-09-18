import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import Message

bot = Bot(token="8197013227:AAGGdLartz7O5E1cUFgHmUgPvA5UVU4jk3Y")
dp = Dispatcher()


@dp.message()
async def cmd_start(message: Message):
    await message.answer('Привет!')


async def main():
    await dp.start_polling(bot)

if __name__ == '__tg_main__':
    asyncio.run(main())