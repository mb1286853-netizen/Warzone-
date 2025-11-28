import logging
import os
import importlib
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

# لود متغیرهای محیطی
load_dotenv()
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("توکن بات در .env پیدا نشد!")

logging.basicConfig(level=logging.INFO)

# ساخت بات و دیسپچر
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# -------------------------------
# لود خودکار همه روترها از پوشه handlers
# -------------------------------
handlers_path = os.path.join(os.path.dirname(__file__), "handlers")
if os.path.isdir(handlers_path):
    for filename in os.listdir(handlers_path):
        if filename.endswith(".py") and filename not in ["__init__.py"]:
            module_name = filename[:-3]  # حذف .py
            try:
                module = importlib.import_module(f"handlers.{module_name}")
                if hasattr(module, "router"):
                    dp.include_router(module.router)
                    print(f"✓ روتر {module_name} با موفقیت لود شد")
                else:
                    print(f"⚠ فایل {filename} router نداره!")
            except Exception as e:
                print(f"✗ خطا در لود {filename}: {e}")
else:
    print("پوشه handlers پیدا نشد!")

# -------------------------------
# تنظیمات وب‌هوک
# -------------------------------
async def on_startup(dispatcher: Dispatcher, bot: Bot):
    webhook_url = f"https://{os.environ['RENDER_EXTERNAL_HOSTNAME']}/webhook"
    await bot.set_webhook(url=webhook_url)
    print(f"Webhook فعال شد: {webhook_url}")
    print("WarZone Bot 24 ساعته و بدون خواب آنلاین شد! ⚔️")

async def on_shutdown(dispatcher: Dispatcher, bot: Bot):
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.session.close()
    print("بات خاموش شد.")

# صفحه اصلی برای تست زنده بودن
async def index(request):
    return web.Response(text="WarZone Bot زنده‌ست! ⚔️")

# -------------------------------
# اجرای سرور
# -------------------------------
def main():
    app = web.Application()
    app["bot"] = bot

    # ثبت استارتاپ و شات‌داون
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    # ثبت وب‌هوک
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path="/webhook")
    app.router.add_get("/", index)

    # پورت Render
    port = int(os.environ.get("PORT", 8000))
    web.run_app(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
