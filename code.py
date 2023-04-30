from aiogram import Bot, Dispatcher
from aiogram.filters import Command, Text
from aiogram.types import Message

import random

user: dict = {'in_game': False,
              'number': None,
              'attempts': None,
              'total_games': 0,
              'wins': 0
              }

api_token: str = '6139815692:AAG586lZubTtxGsauULpDjyHSWetVCF3b-4'

ATTEMPTS: int = 7

bot: Bot = Bot(token=api_token)
dp: Dispatcher = Dispatcher()


def random_number() -> int:
    return random.randint(1, 100)

async def start_filter(message:Message) -> bool:
    return message.text == '/start'


@dp.message(start_filter)
async def process_start_command(message: Message):
    await message.answer('Привет,давай сыграем.\nПомощь- /help')


@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer('/game - начать игру''\n'
                         "Нет - не играть"'\n'
                         '/stat - статистика''\n'
                         "/cancel- выйти из игры"'\n'
                         "можно еще что-нибудь написать")

@dp.message(Command(commands=['stat']))
async def process_stat_command(message: Message):
    x = user['wins']
    y = user['total_games']
    await message.answer(f'побед -{x} \n всего игр - {y}')


@dp.message(Command(commands=['cancel']))
async def process_cancel_command(message:Message):
    if user['in_game'] == True:
        await message.answer('Вышли из игры')
        user['in_game'] = False
    else:
        await message.answer('А мы и так не в игре')


@dp.message(Text(text=['нет', "Нет", "не хочу", "Не хочу"], ignore_case=True))
async def process_negative_answer(message: Message):
    if not user['in_game']:
        await message.answer('а может сыграем?.\nПомощь- /help')
    else:
        await message.answer("Мы же играем, прислыйте предположения")


@dp.message(Command(commands=['game']))
async def process_positive_answer(message: Message):
    if not user['in_game']:
        await message.answer('Хорошо, я загадал число от 1 до 100. Присылайте предположения')
        user["in_game"] = True
        user['number'] = random_number()
        user['attempts'] = ATTEMPTS
    else:
        await message.answer("В игре я могу реагировать только на числа")


@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_numbers_answer(message:Message):


    if user['in_game']:
        if int(message.text) == user['number']:
            await message.answer('Вы угадали')
            user['in_game'] = False
            user['wins'] += 1
            user['total_games'] += 1

        elif int(message.text) > user['number']:
            await message.answer('Мое число меньше')
            user['attempts'] -= 1

        elif int(message.text) < user['number']:
            await message.answer('Мое число больше')
            user['attempts'] -= 1


        if user['attempts'] == 0:
            await message.answer('Попытки кончились, вы проиграли')
            user['in_game'] = False
            user['total_games'] += 1

    else:
        await message.answer('Мы еще не играем, хотите начать?')


@dp.message()
async def send_smth(message: Message):
    if user['in_game']:
        await message.answer('Мы же играем. Пришлите число от 1 до 100')

    else:
        await  message.answer('я хз. спросите /help')



if __name__ == '__main__':
    dp.run_polling(bot)
