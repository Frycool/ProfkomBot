from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
import logging
from aiogram.filters import BaseFilter
from aiogram import F
from aiogram import types


from DataBase import create_table, find_group_id, check_user_id, find_chat_id, create_new_user, change_act, find_fio, \
    change_fio, change_message_thread_id, find_act, make_admin, create_admins_list, delete_admin
from Buttons import leave_req


# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token='7286065305:AAE9aXpq8R5H0jue4pMVaRijCr5reUQwRQw')
dp = Dispatcher()
maingroupid = -1002472571227
admin_ids: list[int] = [0]
create_table()
create_admins_list(admin_ids)

class IsAdmin(BaseFilter):
    def __init__(self, admin_ids: list[int]) -> None:
        # В качестве параметра фильтр принимает список с целыми числами
        self.admin_ids = admin_ids

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.admin_ids

@dp.message(Command(commands=["help"]))
async def start_command(message: Message):
    if message.chat.id == maingroupid:
        await bot.send_message(chat_id=message.chat.id, text='Есть такие команды: \n/start - команда, которая начинает'
                                                             '\n/stop - команда, которая завершает ваш диалог с абобусом '
                                                             'общение с ботом \n/MakeMeAdmin - команда, которая делает вас админом '
                                                             '\n/DeleteMeAsAdmin - команда, которая удаляет вас из списка админов ')
    else:
        await bot.send_message(chat_id=message.chat.id, text='Есть такие команды: \n/start - команда, которая начинает'
                                                             '\n/stop - команда, которая завершает ваш диалог с абобусом ')

@dp.message(Command(commands=["MakeMeAdmin"]))
async def start_command(message: Message):
    if message.chat.id == maingroupid:
        make_admin(message.from_user.id)
        admin_ids.append(message.from_user.id)
        await bot.send_message(chat_id=message.from_user.id, text='Вы теперь админ!')
    else:
        await bot.send_message(chat_id=message.from_user.id, text='Вы не являетесь членом профкома!!!')

@dp.message(Command(commands=["DeleteMeASAdmin"]))
async def start_command(message: Message):
    if message.chat.id == maingroupid:
        delete_admin(message.from_user.id, admin_ids)
        await bot.send_message(chat_id=message.from_user.id, text='Вы все просрали!!!')
    else:
        await bot.send_message(chat_id=message.from_user.id, text='Вы не являетесь членом профкома!!!')

@dp.message(Command(commands=["start"]))
async def start_command(message: Message):
    await leave_req(message)

@dp.message(Command(commands=["stop"]))
async def stop_command(message: Message):
    if find_act(message.from_user.id) == 1 and message.chat.type == 'private':
        change_act(message.from_user.id)
        await bot.send_message(chat_id=maingroupid, text='Пользователь завершил диалог',
                               message_thread_id=find_group_id(message.from_user.id))
        await bot.send_message(chat_id=message.from_user.id, text='Вы закончили диалог с абобусом')
    elif find_act(message.from_user.id) == 0:
        await bot.send_message(chat_id=message.from_user.id, text='У вас нет активного диалога, '
                                                                  'если вы хотите его начать, введите команду /start')

@dp.callback_query(F.data == "leave_req")
async def button_check(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    if check_user_id(user_id) == True and find_act(callback.from_user.id) == 0:

        change_act(callback.from_user.id)
        await callback.message.answer('Задайте ваш вопрос!')

    elif check_user_id(user_id) == True and find_act(callback.from_user.id) == 1:

        await callback.message.answer('Задайте ваш вопрос!')

    else:

        create_new_user(user_id)
        await callback.message.answer('Введите ваше ФИО')

@dp.message(IsAdmin(admin_ids))
async def answer_if_admins_update(message: Message):
    if message.chat.type == 'private':
        await bot.send_message(chat_id=message.from_user.id, text='Ты сам админ из профкома, '
                                                                  'ты зачем вопрос задаешь. Тебе никто не ответит!!!')
    else:

        await bot.send_message(chat_id=find_chat_id(message.message_thread_id), text=message.text)

@dp.message()
async def send_fio(message: Message):

    if find_fio(message.from_user.id) == 0 and message.chat.type == 'private':
        result = await bot.create_forum_topic(chat_id=maingroupid, name=message.text)
        change_fio(message.from_user.id)
        change_message_thread_id(message.from_user.id, result.message_thread_id)
        await bot.send_message(chat_id=message.from_user.id, text='Диалог начался, если вы хотите '
                                                                  'его закончить, напишите команду /stop. '
                                                                  '\nВы все равно получите сообщение от абобуса')

    elif message.chat.id == maingroupid:
        await bot.send_message(chat_id=message.from_user.id, text='Вы пишите из группы профкома, однако не являетесь '
                                                                  'админом, чтобы им стать, напишите команду '
                                                                  '/MakeMeAdmin в главную группу чата')

    elif find_act(message.from_user.id) == 1 and message.chat.type == 'private':
        if message.chat.type != 'private':
            logger.warning(f"Bot received a message in a group chat. Ignoring.")
            return
        message_thread_id = find_group_id(message.from_user.id)
        await bot.send_message(chat_id=maingroupid, text=message.text, message_thread_id=message_thread_id)

    elif find_act(message.from_user.id) == 0 and message.chat.type == 'private':
        await bot.send_message(chat_id=message.from_user.id, text='У вас нет активного диалога, если вы '
                                                                  'хотите его начать, введите команду /start')


if __name__ == '__main__':
    dp.run_polling(bot)
