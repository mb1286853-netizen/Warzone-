from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import OWNER_ID
import re

router = Router()

class Support(StatesGroup):
    waiting = State()

@router.callback_query(F.data == "support")
async def support_start(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        "پیامت رو بنویس و بفرست.\nبه زودی جواب می‌گیری!",
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[[
            types.InlineKeyboardButton("لغو", callback_data="main_menu")
        ]])
    )
    await state.set_state(Support.waiting)

@router.message(Support.waiting)
async def support_msg(message: types.Message, state: FSMContext):
    text = f"""
پیام پشتیبانی جدید

از: {message.from_user.full_name}
یوزرنیم: @{message.from_user.username or "ندارد"}
آیدی: <code>{message.from_user.id}</code>

متن:
{message.text}
    """.strip()
    await message.copy_to(OWNER_ID, caption=text)
    await message.answer("پیامت ارسال شد! به زودی جواب می‌گیری", reply_markup=back_kb("main_menu"))
    await state.clear()

# جواب ادمین
@router.message(F.reply_to_message)
async def admin_reply(message: types.Message):
    if message.from_user.id != OWNER_ID:
        return
    if message.reply_to_message.caption and "پیام پشتیبانی جدید" in message.reply_to_message.caption:
        match = re.search(r"آیدی: <code>(\d+)</code>", message.reply_to_message.caption)
        if match:
            user_id = int(match.group(1))
            await message.copy_to(user_id)
            await message.answer("جواب ارسال شد")
