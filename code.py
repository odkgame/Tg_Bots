from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import F

from PIL import Image

api_token: str = '6139815692:AAG586lZubTtxGsauULpDjyHSWetVCF3b-4'

bot: Bot = Bot(token=api_token)
dp: Dispatcher = Dispatcher()


@dp.message(Command(commands=['start']))
async def process_start_command(message: Message):
    await message.answer('Привет')


@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer('Напиши мне что-нибудь')


@dp.message()
async def send_echo(message: Message):
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text='Ошибка')


if __name__ == '__main__':
    dp.run_polling(bot)
