from aiogram import Router, types

router = Router()

@router.callback_query(lambda c: c.data == "miner")
async def miner_menu(call: types.CallbackQuery):
    text = "⛏ ماینر شما در حال کاره...\nدرآمد هر ساعت: ۵۰۰ ZP"
    kb = types.InlineKeyboardMarkup(inline_keyboard=[[
        types.InlineKeyboardButton("🔙 برگشت", callback_data="back")
    ]])
    await call.message.edit_text(text, reply_markup=kb)
    await call.answer()
