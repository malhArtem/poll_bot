from aiogram import Router, F, types, Bot

router = Router()


@router.message(F.chat_id == config.support_chat, F.reply_message)
async def support(message: types.Message, bot: Bot):
    text = message.text
    await bot.send_message(chat_id="", text=text)
