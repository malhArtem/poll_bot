from aiogram import Router, types, F
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.utils.keyboard import TestCallbackFactory
from db.models.tests import Tests
from db.models.tests_progress import Progress
from db.models.users import Users

router = Router()


@router.message(CommandStart(deep_link=True))
async def start(message: types.Message, command: CommandObject, session):
    print("имя:", message.from_user.first_name)

    args = command.args.split('_')
    if len(args) == 1:
        await Users.add_user(user_id=message.from_user.id,
                             first_name=message.from_user.first_name,
                             last_name=message.from_user.last_name,
                             username=message.from_user.username, session=session)

    elif len(args) == 3 and args[1] == "r":
        await Users.add_user(user_id=message.from_user.id,
                             first_name=message.from_user.first_name,
                             last_name=message.from_user.last_name,
                             username=message.from_user.username, session=session,
                             referral_code=args[2])
        
        progress = await Progress.get_progress(test_id=args[0], user_id=int(args[2]), session=session)
        # if i

    elif len(args) == 3 and args[1] == "c":
        await Users.add_user(user_id=message.from_user.id,
                             first_name=message.from_user.first_name,
                             last_name=message.from_user.last_name,
                             username=message.from_user.username, session=session,
                             referral_company=args[2])

    test = await Tests.get_test(id=int(args[0]), session=session)
    if test is None:
        return await message.answer("Тест не найден")

    builder = InlineKeyboardBuilder()
    builder.button(text="Пройти тест",
                   # callback_data="test",
                   callback_data=TestCallbackFactory(test_id=test.id, question_number=1)
                   )

    await message.answer(text=test.first_message,
                         reply_markup=builder.as_markup())


@router.message(Command("start"))
async def start(message: types.Message, session):
    print("имя:", message.from_user.first_name)
    await message.answer("Вы похоже запустили бот неправильно, перерйдите по полной ссылке, где в конце есть слово start")
    await Users.add_user(user_id=message.from_user.id,
                         first_name=message.from_user.first_name,
                         last_name=message.from_user.last_name,
                         username=message.from_user.username, session=session)


# @router.callback_query(F.data == "test")
# async def test_callback(callback: types.CallbackQuery, session):
#     await callback.message.answer("есть контакт")