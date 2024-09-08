import asyncio

from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from sqlalchemy.ext.asyncio import AsyncSession

from data.engine import sessionmarker, create_db
from data.orm_query import create_question, create_answer
from meddlewares.db import DBMiddleware

TOKEN = '7483944422:AAGuPAsjOH17F4HSOJW7uED26VX_24Hd_3E'

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer(f"Здраствуйте {message.from_user.full_name} какой у вас вопрос?")
    await bot.send_message(chat_id='1526741555', text=message.text)


@dp.message((F.text) & (F.chat.id != 1526741555))
async def question(message: types.Message, session: AsyncSession):
    await create_question(message.chat.id, message.text, session)
    await bot.send_message(chat_id=1526741555, text=message.text)
    await message.answer('<i>Вопрос отправлен</i>', parse_mode=ParseMode.HTML)


async def start_up():
    await create_db()


@dp.message((F.reply_to_message) & (F.chat.id == 1526741555))
async def answer(message: types.Message, session):
    chat_id = await create_answer(message.reply_to_message.text, session)
    await bot.send_message(chat_id=chat_id, text=f"<b>Ответ от техподдержки:</b>\n{message.text}", parse_mode=ParseMode.HTML)
    await message.answer('<i>Ответ отправлен</i>', parse_mode=ParseMode.HTML)


async def main():
    dp.startup.register(start_up)
    dp.update.middleware(DBMiddleware(sessionmarker))
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
