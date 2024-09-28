from aiogram import Router, types, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

router = Router()

class Support(StatesGroup):
    input = State()


@router.message(Command("help"))
async def support(message: types.Message, state: FSMContext):
    text = "Напишите свой вопрос и мы ответим его, как можно быстрее"
    await state.set_state(Support.input)
    await message.answer(text)


@router.message(Support.input)
async def support(message: types.Message, state: FSMContext, bot: Bot):
    if message.photo is not None:
        appeal = message.caption
        await bot.send_photo(chat_id=config.support_chat, photo=message.photo, caption=message.caption)
    else:
        await bot.send_message(chat_id=config.support_chat, text=message.text)

    await state.clear()
    await message.answer("Ваш вопрос отправлен. Мы ответим на него, как можно быстрее.")



