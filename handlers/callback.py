from aiogram import Router
router = Router()
from aiogram import Router, types
from keyboards import main_menu

router = Router()

@router.callback_query(lambda c: c.data == "main_menu")
async def back_to_main(call: types.CallbackQuery):
    await call.message.edit_text("منوی اصلی:", reply_markup=main_menu())
    await call.answer()
