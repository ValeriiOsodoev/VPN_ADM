import asyncio
import json
import os

import asyncssh
from aiogram import Bot, Dispatcher, executor
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN_BOT')
SERVERS = open('servers.json')

SERVERS_VULTR = os.getenv('SERVERS_VULTR')
SERVERS_HETZNER = os.getenv('SERVERS_HETZNER')
SERVERS_GCORE = os.getenv('SERVERS_GCORE')
SERVERS_REGRU = os.getenv('SERVERS_REGRU')

vultr_dict = json.loads(SERVERS_VULTR)
hetzner_dict = json.loads(SERVERS_HETZNER)
gcore_dict = json.loads(SERVERS_GCORE)
regru_dict = json.loads(SERVERS_REGRU)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

button_add_users = KeyboardButton('Добавить пользователя')
button_del_users = KeyboardButton('Удалить пользователя')
button_get_list_users = KeyboardButton('Получить список пользователей')
button_get_list_servers = KeyboardButton('Получить список серверов')
keyboard = ReplyKeyboardMarkup().row(
    button_add_users,
    button_del_users,
    button_get_list_users,
    button_get_list_servers
)


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Выберите действие: ', reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == 'Получить список серверов')
async def get_list_servers(message):
    button_vultr = KeyboardButton('VULTR')
    button_hetzner = KeyboardButton('HETZNER')
    button_gcore = KeyboardButton('GCORE')
    button_regru = KeyboardButton('REGRU')
    keyboard = ReplyKeyboardMarkup().row(
        button_vultr,
        button_hetzner,
        button_gcore,
        button_regru
    )
    await message.answer('Выберите провайдера: ', reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == 'VULTR')
async def get_vultr_servers(message):
    states = []
    for server_name, server_info in vultr_dict.items():
        states.append(asyncio.create_task(get_users_count(*server_info)))
    for i, state in enumerate(states):
        users_count = await state
        if users_count is not None:
            await message.answer(
                'Пользователей на сервере '
                f'{list(vultr_dict.keys())[i]}:{users_count}')
        else:
            await message.answer('Ошибка при подключении к серверу')


@dp.message_handler(lambda message: message.text == 'HETZNER')
async def get_hetzner_servers(message):
    states = []
    for server_name, server_info in hetzner_dict.items():
        states.append(asyncio.create_task(get_users_count(*server_info)))
    for i, state in enumerate(states):
        users_count = await state
        if users_count is not None:
            await message.answer(
                'Пользователей на сервере '
                f'{list(hetzner_dict.keys())[i]}:{users_count}')
        else:
            await message.answer('Ошибка при подключении к серверу')


@dp.message_handler(lambda message: message.text == 'GCORE')
async def get_gcore_servers(message):
    states = []
    for server_name, server_info in gcore_dict.items():
        states.append(asyncio.create_task(get_users_count(*server_info)))
    for i, state in enumerate(states):
        users_count = await state
        if users_count is not None:
            await message.answer(
                'Пользователей на сервере '
                f'{list(gcore_dict.keys())[i]}:{users_count}')
        else:
            await message.answer('Ошибка при подключении к серверу')


@dp.message_handler(lambda message: message.text == 'REGRU')
async def get_regru_servers(message):
    states = []
    for server_name, server_info in regru_dict.items():
        states.append(asyncio.create_task(get_users_count(*server_info)))
    for i, state in enumerate(states):
        users_count = await state
        if users_count is not None:
            await message.answer(
                'Пользователей на сервере '
                f'{list(regru_dict.keys())[i]}:{users_count}')
        else:
            await message.answer('Ошибка при подключении к серверу')


async def get_users_count(ip_address, server_user, server_password):
    try:
        async with asyncssh.connect(
            ip_address,
            username=server_user,
            password=server_password
        ) as conn:
            result = await conn.run('ls /root/*.conf | wc -l', check=True)
            users = (result.stdout.strip())
            return users
    except Exception as Error:
        print(Error)
        return None


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
