from aiogram.client.default import DefaultBotProperties
from sqlalchemy import URL
import asyncio
import logging
from aiogram import Dispatcher, Bot
from bot.handlers import start
from bot.handlers.users import test
# from bot.handlers.users import help
from bot.handlers.admin import create_test
# from bot.handlers.admin import help as admin_help
from bot.handlers.admin import sending
from bot.handlers.admin import stats


from utils.config_reader import config
from bot.utils import commands, middlewares
from utils import logger
from db import create_async_engine, get_session_maker, proceed_schemas, Base



bot_token = config.bot_token.get_secret_value()
admin_id = config.admin_id


logger = logger.logger


async def on_startup(bot: Bot):
    # Функция срабатывающая при запуске бота
    await commands.set_commands(bot)
    try:
        await bot.send_message(admin_id, "Бот запущен")
    except Exception as e:
        logger.error(e)


async def polling_main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    # redis = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=0)


    # Подключение к БД, создание таблиц
    postgres_url = URL.create(
        "postgresql+asyncpg",
        username=config.POSTGRES_USER,
        host=config.POSTGRES_HOST,
        password=config.POSTGRES_PASSWORD.get_secret_value(),
        database=config.POSTGRES_DB,
        port=config.POSTGRES_PORT
    )

    async_engine = create_async_engine(postgres_url)
    session_maker = get_session_maker(async_engine)
    await proceed_schemas(async_engine, Base.metadata)

    # Создание объекта бота и диспетчера
    bot = Bot(bot_token, default=DefaultBotProperties(parse_mode='html'))
    dp = Dispatcher()

    dp.message.middleware(middlewares.CreateSessionMiddleware())
    dp.callback_query.middleware(middlewares.CreateSessionMiddleware())

    dp.include_routers(start.router,
                       create_test.router,
                       # help.router,
                       # admin_help.router,
                       sending.router,
                       # test.router
                       )

    dp.include_router(test.router)


    dp.startup.register(on_startup)
    # запуск бота с пропуском сообщений, которые приходили когда он был выключен
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, session_maker=session_maker)
    logger.error("Бот запущен")

if __name__ == '__main__':
    asyncio.run(polling_main())



