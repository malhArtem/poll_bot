from aiogram import Router, types
from aiogram.filters import Command

from db.models.tests_progress import Progress
from db.models.users import Users

router = Router()

def stats_text(passed, purchased, users, today_users):
    stats = (f"Всего пользователей: {users}"
             f"Новый ползьзователей: {today_users}"
             f"Количество пройденных тестов: {passed}"
             f"Нажато получить полный разбор: {purchased}")
    return stats


@router.message(Command("stats"))
async def stats(message: types.Message, session):
    passed, purchased = await Progress.stats(session)
    users, today_users = await Users.stats(session)
    text = stats_text(passed, purchased, users, today_users)
    await message.answer(text)



