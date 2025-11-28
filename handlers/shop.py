from aiogram import Router, types
from aiogram.filters import Command
from database import get_user, update_user
from keyboards import back_kb
from items import fighters, missiles_normal, missiles_special, missiles_doomsday

router = Router()

@router.callback_query(lambda c: c.data == "shop")
async def shop_menu(call: types.CallbackQuery):
    text = """
فروشگاه

جنگنده‌ها
پهپادها
موشک‌های عادی
موشک‌های ویژه (فقط جم)
موشک‌های آخرالزمانی (ZP + جم)
پدافند و امنیت سایبری

برای خرید بنویس: /buy نام_آیتم
مثال: /buy شبحِ شب
    """.strip()
    await call.message.edit_text(text, reply_markup=back_kb())

# خرید با دستور /buy
@router.message(Command("buy"))
async def buy_item(message: types.Message):
    user = await get_user(message.from_user.id)
    if not user:
        return

    item_name = " ".join(message.text.split()[1:]).strip()
    if not item_name:
        await message.answer("نام آیتم رو بنویس!\nمثال: /buy شبحِ شب")
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

    # موشک‌های عادی
    elif item_name in missiles_normal:
        price = missiles_normal[item_name]["price_zp"]
        if user["zp"] < price:
            await message.answer("ZP کافی نیست!")
            return
        await update_user(message.from_user.id, zp=user["zp"] - price)
        user["missiles"][item_name] = user["missiles"].get(item_name, 0) + 1
        await update_user(message.from_user.id, missiles=user["missiles"])
        await message.answer(f"موشک {item_name} خریداری شد! ✅")

    # موشک‌های ویژه (فقط جم)
    elif item_name in missiles_special:
        price = missiles_special[item_name]["price_gem"]
        if user["gem"] < price:
            await message.answer("جم کافی نیست!")
            return
        await update_user(message.from_user.id, gem=user["gem"] - price)
        user["missiles"][item_name] = user["missiles"].get(item_name, 0) + 1
        await update_user(message.from_user.id, missiles=user["missiles"])
        await message.answer(f"موشک ویژه {item_name} خریداری شد! ✅")

    # موشک‌های آخرالزمانی
    elif item_name in missiles_doomsday:
        zp_price = missiles_doomsday[item_name]["price_zp"]
        gem_price = missiles_doomsday[item_name]["price_gem"]
        if user["zp"] < zp_price or user["gem"] < gem_price:
            await message.answer("ZP یا جم کافی نیست!")
            return
        await update_user(message.from_user.id, zp=user["zp"] - zp_price, gem=user["gem"] - gem_price)
        user["missiles"][item_name] = user["missiles"].get(item_name, 0) + 1
        await update_user(message.from_user.id, missiles=user["missiles"])
        await message.answer(f"موشک آخرالزمانی {item_name} خریداری شد! ☢️")

    else:
        await message.answer("آیتم پیدا نشد! نام دقیق رو بنویس.")
