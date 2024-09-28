from aiogram import Router, types, Bot
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.utils.keyboard import BuyCallbackFactory, PaidCallbackFactory, InviteCallbackFactory, \
    SendAnalysisCallbackFactory
from db.models.tests import Tests
from db.models.tests_progress import Progress

router = Router()


@router.callback_query(BuyCallbackFactory.filter())
async def buy(callback: types.CallbackQuery, callback_data: BuyCallbackFactory, session, bot: Bot):
    await Progress.update_progress(callback_data.test_id, callback.from_user.id, session, purchased_analysis=True)
    text = "Опалатите по этой ссылке"
    builder = InlineKeyboardBuilder()
    builder.button(text="Я оплатил", callback_data=PaidCallbackFactory(test_id=callback_data.test_id,
                                                                       user_id=callback.from_user.id))

    await callback.message.answer(text, reply_markup=builder.as_markup())
    await callback.answer()


@router.callback_query(InviteCallbackFactory.filter())
async def invite(callback: types.CallbackQuery, callback_data: InviteCallbackFactory, session, bot: Bot):
    text = "Отправьте ссылку на бота вашему другу и когда он запустит бота, вы получите файл разбора теста\n\n"
    text += f"https://t.me{await bot.me()}?start={callback_data.test_id}_r_{callback.from_user.id}"

    await callback.message.answer(text)
    await callback.answer()


@router.callback_query(PaidCallbackFactory.filter())
async def paid(callback: types.CallbackQuery, callback_data: PaidCallbackFactory, session, bot: Bot):
    test = await Tests.get_test(callback_data.test_id, session)
    progress = await Progress.get_progress(test_id=callback_data.test_id, user_id=callback_data.user_id, session=session)
    await callback.answer("Сообщение отправлено администраторам")
    text = (f"Пользователь {callback.from_user.full_name}"
            f"Ник: @{callback.from_user.username}"
            f"Прошёл тест: {test.name}"
            f"Набрано баллов: {progress.score}")

    builder = InlineKeyboardBuilder()
    builder.button(text="Отправить результаты", callback_data=SendAnalysisCallbackFactory(test_id=callback_data.test_id,
                                                                                          user_id=callback.from_user.id))

    await bot.send_message(config.chat1 ,text, reply_markup=builder.as_markup())



    await bot.send_message()