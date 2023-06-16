import asyncio
import datetime
import os
import sqlite3
import time

import schedule
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN_BOT')

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


# функция-обработчик команды /start
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    pass


def get_clients_from_database():
    conn = sqlite3.connect('VPN_DB.db')
    cursor = conn.cursor()
    cursor.execute("SELECT Name, End_of_subscription FROM VPN")
    rows = cursor.fetchall()
    clients = []
    for row in rows:
        client = {
            'Name': row[0],
            'End_of_subscription': row[1]
        }
        clients.append(client)
    cursor.close()
    conn.close()
    return clients


async def process_debtors_button_callback(chat_id):
    # Получаем список клиентов из базы данных
    clients = get_clients_from_database()
    # Определяем текущую дату
    today = datetime.date.today()
    # Создаем пустой список должников
    debtors = []
    # Проходимся по каждому клиенту из списка
    for client in clients:
        # Получаем дату подписки из колонки field5
        subscription_date_str = client.get('End_of_subscription')
        if subscription_date_str and subscription_date_str != '-':
            try:
                # Пытаемся преобразовать строку с датой в объект datetime.date
                subscription_date = datetime.datetime.strptime(subscription_date_str, '%d.%m.%Y').date()
                # Вычисляем разницу между текущей датой и датой подписки в днях
                days = (subscription_date - today).days
                # Проверяем, что дата подписки просрочена или просрочится в
                # ближайшие 3 дня
                if days < 0 or days <= 3:
                    # Добавляем клиента в список должников
                    debtor_name = client.get('Name')
                    if debtor_name:
                        debtors.append((debtor_name, subscription_date_str))
            except ValueError:
                # Если не удалось преобразовать дату, пропускаем клиента
                continue
    if debtors:
        # Отправляем список должников в ответном сообщении
        max_message_length = 4096
        message_text = 'Список должников:\n'
        for debtor in debtors:
            debtor_name = debtor[0]
            subscription_date_str = debtor[1]
            if len(message_text + debtor_name + ' - ' + subscription_date_str + '\n') <= max_message_length:
                message_text += debtor_name + ' - ' + subscription_date_str + '\n'
            else:
                try:
                    # Отправляем ответное сообщение с частью списка
                    await bot.send_message(chat_id=chat_id, text=message_text)
                except Exception as e:
                    # Если не удалось отправить сообщение, выводим в консоль ошибку
                    print(f'Error sending message: {e}')
                message_text = debtor_name + ' - ' + subscription_date_str + '\n'
        try:
            # Отправляем последнюю часть списка
            await bot.send_message(chat_id=chat_id, text=message_text)
        except Exception as e:
            # Если не удалось отправить сообщение, выводим в консоль ошибку
            print(f'Error sending message: {e}')
        debtor_count = len(debtors)
        count_message_text = f"Количество должников: {debtor_count}"
        try:
            # Отправляем ответное сообщение с информацией о количестве должников
            await bot.send_message(chat_id=chat_id, text=count_message_text)
        except Exception as e:
            # Если не удалось отправить сообщение, выводим в консоль ошибку
            print(f'Error sending message: {e}')
    else:
        # Отправляем сообщение о том, что нет должников
        message_text = 'Нет должников'
        try:
            # Отправляем ответное сообщение с результатом
            await bot.send_message(chat_id=chat_id, text=message_text)
        except Exception as e:
            # Если не удалось отправить сообщение, выводим в консоль ошибку
            print(f'Error sending message: {e}')


schedule.every().day.at("12:11").do(
    asyncio.create_task,
    process_debtors_button_callback(144227441)
)


async def run_scheduler():
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_scheduler())
