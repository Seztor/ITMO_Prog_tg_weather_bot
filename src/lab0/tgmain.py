import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.state import State, StatesGroup
from src.lab0.app.handlers import handler_router
from src.lab0.tokens.tokens import get_bot_token


async def main():
    bot = Bot(token=get_bot_token())
    dp = Dispatcher()
    dp.include_router(handler_router)
    print('bot started')
    try:
        await dp.start_polling(bot)
    except:
        print('finished')


if __name__ == '__main__':
    asyncio.run(main())
