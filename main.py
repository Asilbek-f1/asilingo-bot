import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardRemove
import asyncio

TOKEN = "8814299645:AAEBGWFxrpPwShUgm7UL4A2wk19bfVJ7Pnk"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()


# /start buyrug'i va inline tugmalar
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    # Oldingi qolib ketgan pastki tugmalarni tozalash
    await message.answer("Menyu yuklanmoqda...", reply_markup=ReplyKeyboardRemove())

    # Inline tugmalar yaratish
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


# Inline tugmalar bosilganda ishlaydigan qism
@dp.callback_query()
async def inline_handler(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    if callback.data == "courses":
        await bot.send_message(user_id, "📚 Asilingo platformasida zamonaviy kurslar tez kunda ishga tushadi!")
    elif callback.data == "feedback":
        await bot.send_message(user_id,
                               "✍️ Taklif va shikoyatlaringizni to'g'ridan-to'g'ri @AsilingoSupport ga yozib qoldirishingiz mumkin.")
    elif callback.data == "vocabulary":
        await bot.send_message(user_id,
                               "🇬🇧 Vocabulary bo'limi: bu yerda siz uchun foydali inglizcha so'zlar va iboralar taqdim etiladi!")

    await callback.answer()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())