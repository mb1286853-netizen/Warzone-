from aiogram import Router, types

router = Router()

@router.message()
async def start_cmd(message: types.Message):
    await message.answer(
        "به WarZone خوش اومدی جنگجو! ⚔️\n\n"
        "بات الان ۱۰۰٪ آنلاینه و جواب می‌ده!\n"
        "بقیه بخش‌ها رو بعداً درست می‌کنیم، الان فقط لذت ببر که راه افتاد!",
        reply_markup=types.ReplyKeyboardRemove()
    )
