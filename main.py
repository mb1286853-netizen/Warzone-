import logging
import os
import importlib
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("توکن بات در .env پیدا نشد!")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# لود خودکار همه روترها
handlers_path = os.path.join(os.path.dirname(__file__), "handlers")
if os.path.isdir(handlers_path):
    for filename in os.listdir(handlers_path):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = filename[:-3]
            try:
                module = importlib.import_module(f"handlers.{module_name}")
                if hasattr(module, "router"):
                    dp.include_router(module.router)
                    print(f"✓ روتر {module_name} لود شد")
            except Exception as e:
                print(f"✗ خطا در {filename}: {e}")

async def on_startup(dispatcher: Dispatcher, bot: Bot):
    try:
        webhook_url = f"https://{os.environ['RENDER_EXTERNAL_HOSTNAME']}{os.environ['RENDER_EXTERNAL_URL_PATH'] or ''}/webhook"
        info = await bot.get_webhook_info()
        if info.url != webhook_url:
            await bot.delete_webhook(drop_pending_updates=True)
            await bot.set_webhook(url=webhook_url, drop_pending_updates=True)
            print(f"✓ وب‌هوک با موفقیت ست شد: {webhook_url}")
        else:
            print(f"وب‌هوک قبلاً ست شده: {webhook_url}")
    except Exception as e:
        print(f"✗ خطا در تنظیم وب‌هوک: {e}")

async def on_shutdown(dispatcher: Dispatcher, bot: Bot):
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.session.close()

async def index(request):
    return web.Response(text="WarZone Bot زنده‌ست! ⚔️")

def main():
    app = web.Application()
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path="/webhook")
    app.router.add_get("/", index)
    port = int(os.environ.get("PORT", 8000))
    web.run_app(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
