from aiogram import Router, types, Bot

from bot.utils.keyboard import SendAnalysisCallbackFactory
from db.models.tests import Tests

router = Router()


@router.callback_query(SendAnalysisCallbackFactory.filter())
async def send_analysis(callback: types.CallbackQuery, callback_data: SendAnalysisCallbackFactory, session, bot: Bot):
    test = await Tests.get_test(callback_data.test_id, session)
    await bot.send_message(callback_data.user_id, test.detailed_analysis)
    await callback.answer()