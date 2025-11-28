from aiogram import Router, types
from aiogram.filters import Command
from database import get_user, update_user
from items import fighters, missiles_normal, missiles_special, missiles_doomsday
from keyboards import back_kb

router = Router()

@router.callback_query(lambda c: c.data == "shop")
async def shop_menu(call: types.CallbackQuery):
    user = await get_user(call.from_user.id)
    text = f"🛒 فروشگاه\nZP: {user['zp']:,} | Gem: {user['gem']}\n\n/buy [نام آیتم]"
    await call.message.edit_text(text, reply_markup=back_kb())

@router.message(Command("buy"))
async def buy_item(message: types.Message):
    user = await get_user(message.from_user.id)
    item_name = " ".join(message.text.split()[1:]).strip()
    if not item_name:
        await message.answer("نام آیتم رو بنویس! مثال: /buy شبحِ شب")
        return

    # جنگنده‌ها
    if item_name in fighters:
        price = fighters[item_name]["price"]
        if user["zp"] < price:
            await message.answer("ZP کافی نیست!")
            return
        await update_user(message.from_user.id, zp=user["zp"] - price)
        user["fighters"][item_name] = user["fighters"].get(item_name, 0) + 1
        await update_user(message.from_user.id, fighters=user["fighters"])
        await message.answer(f"جنگنده {item_name} خریداری شد! ✅")
    # ... بقیه خریدها مثل قبل (موشک‌ها و ...)
    # (کد کامل تو ZIP هست)
