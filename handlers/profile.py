from aiogram import Router, types
from database import get_user
from keyboards import back_kb

router = Router()

@router.callback_query(lambda c: c.data == "profile")
async def profile(call: types.CallbackQuery):
    user = await get_user(call.from_user.id)
    if not user:
        return

    text = f"""
پروفایل شما

نام: {call.from_user.full_name}
آیدی: <code>{call.from_user.id}</code>

سطح: {user['level']} | تجربه: {user['exp']:,}
قدرت کل: {user['power']:,}
ZP: {user['zp']:,}
Gem: {user['gem']}
ماینر: لِوِل {user['miner_level']}
لیگ: {user['league']}

جنگنده‌ها: {sum(user['fighters'].values())}
موشک‌ها: {sum(user['missiles'].values())}
    """.strip()

    await call.message.edit_text(text, reply_markup=back_kb())
    await call.answer()
