from aiogram import Router, types
from aiogram.filters import Command
from database import create_user
from keyboards import main_menu
from utils import check_membership
from config import CHANNEL_ID

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await create_user(message.from_user.id)
    
    if not await check_membership(message.from_user.id):
        kb = types.InlineKeyboardMarkup(inline_keyboard=[[
            types.InlineKeyboardButton("عضویت در کانال", url=f"https://t.me/{CHANNEL_ID[1:]}")
        ]])
        await message.answer("برای ادامه باید در کانال عضو شی!", reply_markup=kb)
        return
    
    await message.answer("به WarZone خوش اومدی جنگجو! ⚔️", reply_markup=main_menu())
