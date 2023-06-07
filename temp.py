import asyncio
import json
import os
import time
from io import BytesIO

import asyncssh
import paramiko
import qrcode
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN_BOT')

ID_ADMIN = os.getenv('ID_ADMIN')
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


button_add = KeyboardButton('Выбрать сервер')
keyboard = ReplyKeyboardMarkup(resize_keyboard=True).row(button_add)


class State(StatesGroup):
    waiting_for_name = State()


@dp.message_handler(commands=['start'], state="*")
async def start(message, state: FSMContext):
    await state.finish()
    if str(message.from_user.id) in ID_ADMIN:
        await message.answer('Выберите действие: ', reply_markup=keyboard)
    else:
        await message.answer(
            'У вас нет разрешения на выполнение этой команды.'
        )


@dp.message_handler(
    lambda message: message.text == 'Выбрать сервер'
)
async def keyboard_create(message):
    if str(message.from_user.id) in ID_ADMIN:
        button_vultr = KeyboardButton('VULTR')
        button_hetzner = KeyboardButton('HETZNER')
        button_gcore = KeyboardButton('GCORE')
        button_regru = KeyboardButton('REGRU')
        button_main_menu = KeyboardButton('В главное меню')
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True).row(
            button_vultr,
            button_hetzner,
            button_gcore,
            button_regru,
            button_main_menu
        )
        await message.answer('Выберите провайдера: ', reply_markup=keyboard)
    else:
        await message.answer(
            'У вас нет разрешения на выполнение этой команды.'
        )


@dp.message_handler(lambda message: message.text in [
    'VULTR', 'HETZNER', 'GCORE', 'REGRU'
])
async def get_users(message: types.Message):
    if str(message.from_user.id) in ID_ADMIN:
        providers = message.text.strip().lower()
        if providers == 'vultr':
            provider_dict = vultr_dict
        elif providers == 'hetzner':
            provider_dict = hetzner_dict
        elif providers == 'gcore':
            provider_dict = gcore_dict
        elif providers == 'regru':
            provider_dict = regru_dict
        else:
            await message.answer(
                'Выбран не корректный провайдер.'
            )
            return

        for server_name, server_info in provider_dict.items():
            # получаем количество пользователей
            users_count_task = asyncio.create_task(
                get_users_count(*server_info)
            )
            # получаем список пользователей
            users_list_task = asyncio.create_task(
                get_users_list(*server_info)
            )
            # ожидаем результаты обоих задач
            users_count = await users_count_task
            users_list = await users_list_task
            # если данные получены, выводим их в чат
            # если данные не получены, выводим ошибку в чат
            if users_count is not None:
                keyboard = types.InlineKeyboardMarkup()
                button_add = types.InlineKeyboardButton(
                    text="Добавить пользователя",
                    callback_data=f"add {providers} {server_name}"
                )
                button_del = types.InlineKeyboardButton(
                    text="Удалить пользователя",
                    callback_data=f"del {providers} {server_name}"
                )
                keyboard.add(button_add, button_del)
                await message.answer(
                    f'<b>Сервер {server_name}</b>\n\n'
                    f'Пользователи сервера:\n\n<b>{users_list}</b>\n\n'
                    f'Количество пользователей: <b>{users_count}</b>\n\n',
                    reply_markup=keyboard,
                    parse_mode='HTML'
                )
            else:
                await message.answer(
                    f'Ошибка при подключении к серверу {server_name}'
                )
    else:
        await message.answer(
            'У вас нет разрешения на выполнение этой команды.'
        )


providers_dict = {
    'vultr': vultr_dict,
    'hetzner': hetzner_dict,
    'gcore': gcore_dict,
    'regru': regru_dict
}


@dp.callback_query_handler(lambda query: query.data.startswith('add'), state="*")
async def add_user_to_server(query: types.CallbackQuery, state: FSMContext):
    user_id = str(query.from_user.id)
    if user_id not in ID_ADMIN:
        await query.answer(
            'У вас нет прав для выполнения этой команды.',
            show_alert=True
        )
        return

    _, provider, server_name = query.data.split()
    provider_dict = providers_dict.get(provider)

    server_info = provider_dict.get(server_name)
    if isinstance(server_info, list):
        ip = server_info[0]
        user = server_info[1]
        passwd = server_info[2]

    await bot.send_message(
        chat_id=query.from_user.id,
        text='Введите имя пользователя для добавления '
        f'на сервер {server_name}:',
    )

    # Переключаемся в состояние ожидания ввода текста
    await state.set_state(State.waiting_for_name.state)
    user_name = await state.get_data()
    print(user_name)

    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, username=user, password=passwd)
    remote_shell = ssh.invoke_shell()
    remote_shell.send('./wireguard-install.sh\n')
    time.sleep(0.5)
    remote_shell.send('1\n')
    time.sleep(0.5)
    remote_shell.send(f'{user_name}\n')
    time.sleep(0.5)
    remote_shell.sendall('\n')
    time.sleep(0.5)
    remote_shell.sendall('\n')
    config_path = f'/root/wg0-client-{user_name}.conf'
    time.sleep(3)

    await send_qr_code(query.from_user.id, config_path, ssh)

    await bot.send_message(
        query.from_user.id,
        f"Пользователь {user_name} успешно добавлен на сервер {server_name}."
    )


async def send_qr_code(chat_id, config_path, ssh):
    """Генерируем QR-код на удаленном сервере."""
    stdin, stdout, stderr = ssh.exec_command(f'cat {config_path}')
    data = stdout.read().decode().strip()

    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # создаем буфер для хранения QR-кода
    with BytesIO() as output:
        img.save(output)
        contents = output.getvalue()

        # отправляем QR-код
        await bot.send_photo(chat_id, contents)


async def get_users_list(ip_address, server_user, server_password):
    try:
        async with asyncssh.connect(
            ip_address,
            username=server_user,
            password=server_password
        ) as conn:
            result = await conn.run('ls -tr wg0-client-*.conf | grep -oP "(?<=wg0-client-).*(?=.conf)"\n', check=True)
            users = (result.stdout.strip())
            return users
    except Exception as Error:
        print(Error)
        return None


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


@dp.message_handler(lambda message: message.text == 'В главное меню')
async def button_main_menu(message):
    if str(message.from_user.id) in ID_ADMIN:
        await message.answer('Выберите действие:', reply_markup=keyboard)
    else:
        await message.answer(
            'У вас нет разрешения на выполнение этой команды.'
        )


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
