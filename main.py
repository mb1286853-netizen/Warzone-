import logging
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("توکن پیدا نشد!")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# هندلرهای اصلی
from handlers import start, profile, attack, shop, boxes, miner, defense, support, callback

# ثبت همه روترها
dp.include_router(start.router)
dp.include_router(profile.router)
dp.include_router(attack.router)
dp.include_router(shop.router)
dp.include_router(boxes.router)
dp.include_router(miner.router)
dp.include_router(defense.router)
dp.include_router(support.router)
dp.include_router(callback.router)

async def on_startup(dispatcher: Dispatcher, bot: Bot):
    webhook_url = f"https://{os.environ['RENDER_EXTERNAL_HOSTNAME']}/webhook"
    await bot.set_webhook(url=webhook_url)
    print(f"Webhook فعال شد: {webhook_url}")
    print("WarZone Bot 24 ساعته و بدون خواب آنلاین شد! ⚔️")

async def on_shutdown(dispatcher: Dispatcher, bot: Bot):
    await bot.delete_webhook()
    await bot.session.close()

async def index(request):
    return web.Response(text="WarZone Bot زنده‌ست! ⚔️")

def main():
    app = web.Application()
    app["bot"] = bot
    app["dp"] = dp

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path="/webhook")
    app.router.add_get("/", index)

    port = int(os.environ.get("PORT", 8000))
    web.run_app(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
