from aiogram import Router, types

router = Router()

@router.callback_query(lambda c: c.data == "back")
async def go_back(call: types.CallbackQuery):
    from keyboards import main_menu  # فقط این یکی اوکیه اگه main_menu داری
    try:
        await call.message.edit_text("به منوی اصلی برگشتی جنگجو! ⚔️", reply_markup=main_menu())
    except:
        await call.message.edit_text("به منوی اصلی برگشتی!", reply_markup=main_menu())
    await call.answer()
