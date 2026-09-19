import logging
import os
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardRemove
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

TOKEN = os.environ["BOT_TOKEN"]
WEBHOOK_HOST = os.environ["WEBHOOK_HOST"]
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"
PORT = int(os.environ.get("PORT", 10000))

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Menyu yuklanmoqda...", reply_markup=ReplyKeyboardRemove())

    builder = InlineKeyboardBuilder()
    builder.button(text="📞 Biz bilan bog'lanish", url="https://t.me/AsilingoSupport")
    builder.button(text="📚 Kurslar", callback_data="courses")
    builder.button(text="📢 Asosiy Kanal", url="https://t.me/asilingospeak")
    builder.button(text="✍️ Taklif va Shikoyatlar", callback_data="feedback")
    builder.button(text="🇬🇧 Vocabulary", callback_data="vocabulary")
    builder.adjust(1, 2, 2)

    await message.answer(
        "Assalomu alaykum! Asilingo rasmiy botiga xush kelibsiz. Marhamat, quyidagi bo'limlardan birini tanlang:",
        reply_markup=builder.as_markup()
    )


@dp.callback_query()
async def inline_handler(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    if callback.data == "courses":
        await bot.send_message(user_id, "📚 Asilingo platformasida zamonaviy kurslar tez kunda ishga tushadi!")
    elif callback.data == "feedback":
        await bot.send_message(user_id, "✍️ Taklif va shikoyatlaringizni to'g'ridan-to'g'ri @AsilingoSupport ga yozib qoldirishingiz mumkin.")
    elif callback.data == "vocabulary":
        await bot.send_message(user_id, "🇬🇧 Vocabulary bo'limi: bu yerda siz uchun foydali inglizcha so'zlar va iboralar taqdim etiladi!")

    await callback.answer()


async def health_check(request):
    return web.Response(text="Asilingo bot is running ✅")


async def on_startup(bot: Bot):
    await bot.set_webhook(WEBHOOK_URL)
    logging.info(f"Webhook o'rnatildi: {WEBHOOK_URL}")


def main():
    app = web.Application()
    app.router.add_get("/", health_check)

    dp.startup.register(on_startup)

    webhook_handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
    webhook_handler.register(app, path=WEBHOOK_PATH)

    setup_application(app, dp, bot=bot)

    web.run_app(app, host="0.0.0.0", port=PORT)


if __name__ == "__main__":
    main()
