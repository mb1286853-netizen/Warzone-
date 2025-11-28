from aiogram import Router, types
from database import get_user, update_user
import random

router = Router()

@router.message(lambda m: m.reply_to_message)
async def attack_reply(message: types.Message):
    attacker = message.from_user.id
    target = message.reply_to_message.from_user.id

    if attacker == target:
        await message.answer("نمی‌تونی به خودت حمله کنی!")
        return

    att_user = await get_user(attacker)
    tar_user = await get_user(target)
    if not att_user or not tar_user:
        return

    damage = random.randint(800, 1800)
    loot = int(damage * 0.08)

    await update_user(attacker, zp=att_user['zp'] + loot)
    await update_user(target, zp=max(0, tar_user['zp'] - loot))

    await message.answer(f"""
حمله موفق!

دمیج: {damage:,} ⚔️
غارت ZP: +{loot:,} 💰
    """.strip())
