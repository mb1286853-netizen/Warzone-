import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config import TOKEN
import database

# همه هندلرها
from handlers import (
    start,
    profile,
    attack,
    shop,
    boxes,
    miner,
    defense,
    support,
    callback
)

# لاگ برای دیباگ (در Render هم نشون می‌ده)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# شروع بات
async def on_startup():
    await database.init_db()
    print("="*50)
    print("WarZone Bot کاملاً آنلاین شد!")
    print("جنگنده‌ها آماده، موشک‌ها بارگذاری شدن!")
    print("پشتیبانی، جعبه شانس، ماینر، پدافند — همه چیز فعاله!")
    print("="*50)

async def main():
    # ثبت استارتاپ
    dp.startup.register(on_startup)

    # اضافه کردن همه هندلرها
    dp.include_router(start.router)
    dp.include_router(profile.router)
    dp.include_router(attack.router)
    dp.include_router(shop.router)
    dp.include_router(boxes.router)
    dp.include_router(miner.router)
    dp.include_router(defense.router)
    dp.include_router(support.router)
    dp.include_router(callback.router)

    print("در حال اتصال به تلگرام...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
