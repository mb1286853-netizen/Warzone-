from aiogram import Router, types

router = Router()

@router.callback_query(lambda c: c.data == "support")
async def support_menu(call: types.CallbackQuery):
    text = "🆘 پشتیبانی\nبه زودی فعال می‌شه!"
    kb = types.InlineKeyboardMarkup(inline_keyboard=[[
        types.InlineKeyboardButton("🔙 برگشت", callback_data="back")
    ]])
    await call.message.edit_text(text, reply_markup=kb)
    await call.answer()
