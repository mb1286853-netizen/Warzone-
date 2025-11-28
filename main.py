import os
import importlib
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# توکن مستقیم از محیط (دیگه dotenv هم لازم نیست)
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("TOKEN پیدا نشد!")

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# فقط start رو دستی لود می‌کنیم — بقیه هر چی شد شد
try:
    from handlers.start import router as start_router
    dp.include_router(start_router)
    print("✓ فقط start لود شد — بقیه مهم نیست")
except Exception as e:
    print(f"حتی start هم لود نشد: {e}")

# وب‌هوک اجباری
async def on_startup(*_):
    url = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME', 'warzone-xgnp.onrender.com')}/webhook"
    await bot.set_webhook(url=url, drop_pending_updates=True)
    print(f"وب‌هوک ست شد: {url}")

async def index(_):
    return web.Response(text="بات زنده‌ست!")

app = web.Application()
dp.startup.register(on_startup)
SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path="/webhook")
app.router.add_get("/", index)

web.run_app(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
