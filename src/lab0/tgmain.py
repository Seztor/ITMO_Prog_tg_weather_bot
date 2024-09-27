import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.state import State, StatesGroup
from src.lab0.app.handlers import handler_router



async def main():
    bot = Bot(token=open('C:/Users/pavel/PycharmProjects/tg_bot/src/lab0/tokens/TOKEN_BOT.txt').readline().strip())
    dp = Dispatcher()
    dp.include_router(handler_router)
    print('bot started')
    try:
        await dp.start_polling(bot)
    except:
        print('finished')


if __name__ == '__main__':
    asyncio.run(main())
