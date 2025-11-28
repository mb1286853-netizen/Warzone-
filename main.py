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
    raise ValueError("توکن پیدا نشد!")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# لود خودکار همه روترها
print("شروع لود روترها...")
for file in os.listdir("handlers"):
    if file.endswith(".py") and file != "__init__.py":
        name = file[:-3]
        try:
            mod = importlib.import_module(f"handlers.{name}")
            if hasattr(mod, "router"):
                dp.include_router(mod.router)
                print(f"✓ روتر {name} لود شد")
        except Exception as e:
            print(f"✗ خطا در {name}: {e}")

async def on_startup(*args):
    try:
        url = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME', 'warzone-xgnp.onrender.com')}/webhook"
        await bot.delete_webhook(drop_pending_updates=True)
        await bot.set_webhook(url=url)
        print(f"وب‌هوک ست شد → {url}")
    except Exception as e:
        print(f"خطا در وب‌هوک: {e}")

async def index(_):
    return web.Response(text="WarZone Bot زنده‌ست! ⚔️")

app = web.Application()
dp.startup.register(on_startup)
SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path="/webhook")
app.router.add_get("/", index)

if __name__ == "__main__":
    web.run_app(app, port=int(os.environ.get("PORT", 8000)))
