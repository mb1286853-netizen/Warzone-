from aiogram import Router
router = Router()
from aiogram import Router, types
from database import get_user, update_user
import time

router = Router()

miner_cost = [0, 200, 450, 800, 1300, 2000, 3000, 4500, 6500, 9000, 11000, 12500, 13500, 14500, 15000]  # لِوِل ۱→۲ = ۲۰۰ و ... تا ۱۵

@router.callback_query(lambda c: c.data == "miner")
async def miner_menu(call: types.CallbackQuery):
    user = await get_user(call.from_user.id)
    level = user['miner_level']
    produce = level * 120  # هر ساعت

    text = f"""
ماینر شما
سطح فعلی: {level}
تولید هر ساعت: {produce:,} ZP
سقف هر ۳ ساعت

برای ارتقا به لِوِل {level+1}: {miner_cost[level]:,} ZP
    """.strip()

    kb = [
        [types.InlineKeyboardButton("برداشت", callback_data="miner_claim")],
    ]
    if level < 15:
        kb.append([types.InlineKeyboardButton("ارتقا ⬆️", callback_data="miner_upgrade")])
    kb.append([types.InlineKeyboardButton("↩️ بازگشت", callback_data="main_menu")])

    await call.message.edit_text(text, reply_markup=types.InlineKeyboardMarkup(inline_keyboard=kb))

@router.callback_query(lambda c: c.data == "miner_upgrade")
async def miner_upgrade(call: types.CallbackQuery):
    user = await get_user(call.from_user.id)
    level = user['miner_level']
    if level >= 15:
        await call.answer("ماینر مکس شده!", show_alert=True)
        return
    cost = miner_cost[level]
    if user['zp'] < cost:
        await call.answer("ZP کافی نیست!", show_alert=True)
        return

    await update_user(call.from_user.id, zp=user['zp'] - cost, miner_level=level + 1)
    await call.answer(f"ماینر به لِوِل {level+1} ارتقا یافت! ✅", show_alert=True)
