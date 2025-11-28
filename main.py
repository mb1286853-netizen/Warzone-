import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, run_app
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiohttp import web
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID", "7664487388"))
CHANNEL_ID = os.getenv("CHANNEL_ID", "@Warezone_bot")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# اینجا همه handlers هات رو ایمپورت کن
from handlers import start, profile, attack, shop, boxes, miner, defense, support, callback

async def on_startup(app):
    await bot.delete_webhook(drop_pending_updates=True)
    webhook_url = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/webhook"
    await bot.set_webhook(webhook_url)
    print(f"Webhook تنظیم شد: {webhook_url}")
    print("WarZone Bot ۲۴ ساعته و بدون خواب آنلاین شد! ⚔️")

def main():
    dp.startup.register(on_startup)
    
    # همه router ها
    dp.include_router(start.router)
    dp.include_router(profile.router)
    dp.include_router(attack.router)
    dp.include_router(shop.router)
    dp.include_router(boxes.router)
    dp.include_router(miner.router)
    dp.include_router(defense.router)
    dp.include_router(support.router)
    dp.include_router(callback.router)

    app = web.Application()
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path="/webhook")
    app.router.add_get("/", lambda _: web.Response(text="WarZone Bot زنده‌ست! ⚔️"))
    
    port = int(os.getenv("PORT", 8000))
    web.run_app(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
