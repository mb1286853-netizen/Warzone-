from aiogram import Router, types
from database import get_user, update_user
from items import missiles_normal
import time
import random

router = Router()

@router.callback_query(lambda c: c.data == "boxes")
async def boxes_menu(call: types.CallbackQuery):
    user = await get_user(call.from_user.id)
    now = int(time.time())

    text = "جعبه شانس 🎁\n\n"
    # جعبه برنزی (رایگان – هر ۲۴ ساعت)
    if now - user['last_free_box'] >= 86400:
        text += "جعبه برنزی (رایگان) ← آماده!\n"
    else:
        remain = 86400 - (now - user['last_free_box'])
        text += f"جعبه برنزی ← {remain//3600}ساعت و {(remain%3600)//60}دقیقه\n"

    text += "\nجعبه نقره‌ای ← 18,000 ZP\n"
    text += "جعبه طلایی ← 4 جم\n"
    text += "جعبه الماس ← 10 جم\n"
    text += "جعبه افسانه‌ای ← 25 جم\n\n"

    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton("جعبه برنزی", callback_data="box_bronze")],
        [types.InlineKeyboardButton("جعبه نقره‌ای", callback_data="box_silver")],
        [types.InlineKeyboardButton("جعبه طلایی", callback_data="box_gold")],
        [types.InlineKeyboardButton("جعبه الماس", callback_data="box_diamond")],
        [types.InlineKeyboardButton("جعبه افسانه‌ای", callback_data="box_legend")],
        [types.InlineKeyboardButton("↩️ بازگشت", callback_data="main_menu")]
    ])

    await call.message.edit_text(text, reply_markup=kb)

# باز کردن جعبه برنزی
@router.callback_query(lambda c: c.data == "box_bronze")
async def open_bronze(call: types.CallbackQuery):
    user = await get_user(call.from_user.id)
    now = int(time.time())
    if now - user['last_free_box'] < 86400:
        await call.answer("هنوز وقتش نشده!", show_alert=True)
        return

    reward_zp = random.randint(800, 3000)
    await update_user(call.from_user.id, zp=user['zp'] + reward_zp, last_free_box=now)
    await call.message.edit_text(f"جعبه برنزی باز شد!\nجایزه: {reward_zp:,} ZP 💰")
    await call.answer()
