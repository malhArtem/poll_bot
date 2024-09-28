import asyncio

from aiogram import Router, F
from aiogram.exceptions import TelegramRetryAfter, TelegramForbiddenError
from aiogram.filters import Command
from aiogram.types import Message

from db.models.users import Users
from utils.logger import logger

router = Router()


@router.message(Command("send"), F.reply_to_message)
async def sending(message: Message, session_maker):
    successfully = 0
    users = await Users.get_users(session_maker)
    for user in users:
        try:
            await message.reply_to_message.send_copy(user.user_id)
            successfully += 1
            await asyncio.sleep(0.05)
        except TelegramRetryAfter:
            await asyncio.sleep(1)
            await message.reply_to_message.send_copy(user.user_id)
            successfully += 1
        except TelegramForbiddenError:
            pass

        except Exception as e:
            logger.error(e)

    text = f"Рассылка была отправлена. Сообщение получили {successfully} пользователей "
    await message.answer(text)
