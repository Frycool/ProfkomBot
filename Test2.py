from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
import logging
from aiogram.filters import BaseFilter
from aiogram import F
from aiogram import types
import sqlite3

from DataBase import create_table, find_group_id, check_user_id, find_chat_id, create_new_user, change_act, find_fio, \
    change_fio, change_message_thread_id, find_act
from Buttons import leave_req


# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token='7286065305:AAE9aXpq8R5H0jue4pMVaRijCr5reUQwRQw')
dp = Dispatcher()
maingroupid = -1002472571227
admin_ids: list[int] = [1615158152]
create_table()



# Собственный фильтр, проверяющий юзера на админа
class IsAdmin(BaseFilter):
    def __init__(self, admin_ids: list[int]) -> None:
        # В качестве параметра фильтр принимает список с целыми числами
        self.admin_ids = admin_ids

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.admin_ids

@dp.message(Command(commands=["start"]))
async def start_command(message: Message):
    await leave_req(message)

@dp.callback_query(F.data == "leave_req")
async def button_check(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    if check_user_id(user_id) == True:
        change_act(user_id)
        await callback.message.answer('Задайте ваш вопрос!')

    else:
        create_new_user(user_id)
        await callback.message.answer('Введите ваше ФИО')

@dp.message(IsAdmin(admin_ids))
async def answer_if_admins_update(message: Message):
    if message.from_user.is_bot:
        logger.warning("Bot tried to send a message to itself. Ignoring.")
        return

    user_id = find_chat_id(message.message_thread_id)

    await bot.send_message(chat_id=user_id, text=message.text)

@dp.message()
async def send_fio(message: Message):
    if find_fio(message.from_user.id) == 0 and message.chat.type == 'private':
        result = await bot.create_forum_topic(chat_id=maingroupid, name=message.text)
        change_fio(message.from_user.id)
        change_message_thread_id(message.from_user.id, result.message_thread_id)
        await bot.send_message(chat_id=message.from_user.id, text='Диалог начался, если вы хотите его закончить, напишите команду /stop. \nВы все равно получите сообщение от абобуса')
    else:
        if find_act(message.from_user.id) == 1:
            if message.chat.type != 'private':
                logger.warning(f"Bot received a message in a group chat. Ignoring.")
                return
        message_thread_id = find_group_id(message.from_user.id)
        await bot.send_message(chat_id=maingroupid, text=message.text, message_thread_id=message_thread_id)


if __name__ == '__main__':
    dp.run_polling(bot)