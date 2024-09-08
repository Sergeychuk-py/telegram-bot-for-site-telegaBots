from keyboards import markup
from aiogram import Bot, Router, F, types
from aiogram.filters import CommandStart

router_handlers = Router()


@router_handlers.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer(f"Здраствуйте {message.from_user.full_name}", reply_markup=markup())


@router_handlers.message(F.text == 'Поддержка')
async def forward_message_to_owner(message: types.Message, bot: Bot):
    owner_id = "1526741555"
    await bot.forward_message(chat_id=owner_id, from_chat_id=message.chat.id, message_id=message.message_id)
