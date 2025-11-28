from aiogram import Router, types
from database import get_user, update_user

router = Router()

# قیمت هر لِوِل (همه با ZP)
defense_prices = {
    "سپر-۹۵": 8000,
    "سدیفاکتور": 12000,
    "توربوشیلد": 18000,
    "لایه نوری": 25000,
    "فایروال سایبری": 22000,
    "هوش مصنوعی دفاعی": 40000,
}

@router.callback_query(lambda c: c.data == "defense")
async def defense_menu(call: types.CallbackQuery):
    user = await get_user(call.from_user.id)
    defs = user.get("defenses", {})

    text = "پدافند و امنیت سایبری 🛡️\n\n"
    text += f"سپر-۹۵: لِوِل {defs.get('سپر-۹۵', 0)}/۱۰\n"
    text += f"سدیفاکتور: لِوِل {defs.get('سدیفاکتور', 0)}/۸\n"
    text += f"توربوشیلد: لِوِل {defs.get('توربوشیلد', 0)}/۷\n"
    text += f"لایه نوری: لِوِل {defs.get('لایه نوری', 0)}/۶\n"
    text += f"فایروال سایبری: لِوِل {defs.get('فایروال سایبری', 0)}/۸\n"
    text += f"هوش مصنوعی دفاعی: لِوِل {defs.get('هوش مصنوعی دفاعی', 0)}/۵\n\n"
    text += "برای ارتقا بنویس: /upgrade نام_پدافند\nمثال: /upgrade سپر-۹۵"

    await call.message.edit_text(text, reply_markup=back_kb())

# دستور ارتقا پدافند
@router.message(lambda m: m.text and m.text.startswith("/upgrade "))
async def upgrade_defense(message: types.Message):
    user = await get_user(message.from_user.id)
    name = message.text[9:].strip()  # بعد از /upgrade

    if name not in defense_prices:
        await message.answer("اسم پدافند اشتباهه!")
        return

    current = user["defenses"].get(name, 0)
    max_levels = {"سپر-۹۵":10, "سدیفاکتور":8, "توربوشیلد":7, "لایه نوری":6,
                  "فایروال سایبری":8, "هوش مصنوعی دفاعی":5}
    
    if current >= max_levels[name]:
        await message.answer(f"{name} مکس شده!")
        return

    cost = defense_prices[name] * (current + 1)  # هر لِوِل گرون‌تر
    if user["zp"] < cost:
        await message.answer("ZP کافی نیست!")
        return

    await update_user(message.from_user.id, zp=user["zp"] - cost)
    new_defs = user["defenses"]
    new_defs[name] = current + 1
    await update_user(message.from_user.id, defenses=new_defs)

    await message.answer(f"{name} به لِوِل {current + 1} ارتقا یافت! 🛡️")
