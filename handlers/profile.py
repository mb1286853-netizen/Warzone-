from aiogram import Router, types

router = Router()

@router.callback_query(lambda c: c.data == "profile")
async def show_profile(call: types.CallbackQuery):
    # فعلاً ساده، بعداً database رو وصل می‌کنیم
    text = f"""
👤 پروفایل شما

نام: {call.from_user.full_name}
آیدی: <code>{call.from_user.id}</code>

سطح: 1
ZP: 0
Gem: 0
لیگ: برنز
    """.strip()
    kb = types.InlineKeyboardMarkup(inline_keyboard=[[
        types.InlineKeyboardButton("🔙 برگشت", callback_data="back")
    ]])
    await call.message.edit_text(text, reply_markup=kb)
    await call.answer()
