from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
import logging
from aiogram.filters import BaseFilter
import sqlite3

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token='7286065305:AAE9aXpq8R5H0jue4pMVaRijCr5reUQwRQw')
dp = Dispatcher()
maingroupid = -1002472571227
users = {}
admin_ids: list[int] = [1615158152]

# Собственный фильтр, проверяющий юзера на админа
class IsAdmin(BaseFilter):
    def __init__(self, admin_ids: list[int]) -> None:
        # В качестве параметра фильтр принимает список с целыми числами
        self.admin_ids = admin_ids

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.admin_ids

@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    global users

    user_id = message.from_user.id

    if user_id not in users:
        users[user_id] = {
            'them_id': 0,
        }


        first_name = message.from_user.first_name
        last_name = message.from_user.last_name

        if last_name is None:
            text = f"{first_name} оставил/a заявку:"
            name = first_name
        else:
            text = f"{first_name} {last_name} оставил/a заявку:"
            name = f"{first_name} {last_name}"

        # Создаем тему на форуме и получаем идентификатор потока
        result = await bot.create_forum_topic(chat_id=maingroupid, name=name)

        # Сохраняем идентификатор потока сообщений (message_thread_id)
        users[user_id]['them_id'] = result.message_thread_id

        # Отправляем сообщение с использованием идентификатора потока сообщений
        await bot.send_message(chat_id=maingroupid, text=text, message_thread_id=users[user_id]['them_id'])
        print(users[user_id]['them_id'])

@dp.message(IsAdmin(admin_ids))
async def answer_if_admins_update(message: Message):
    global users

    if message.from_user.is_bot:
        logger.warning("Bot tried to send a message to itself. Ignoring.")
        return

    them_id = message.message_thread_id

    user_id = next((k for k, v in users.items() if v['them_id'] == them_id), None)

    await bot.send_message(chat_id=user_id, text=message.text)

@dp.message()
async def send_message(message: Message):
    global users

    if message.chat.type != 'private':
        logger.warning(f"Bot received a message in a group chat. Ignoring.")
        return

    user_id = message.from_user.id  # Получаем user_id из сообщения

    await bot.send_message(chat_id=maingroupid, text=message.text, message_thread_id=users[user_id]['them_id'])

if __name__ == '__main__':
    dp.run_polling(bot)

