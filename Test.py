from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import F
from aiogram import types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from DataBase import create_table, find_group_id, check_user_id, find_chat_id, create_new_user, change_act, \
     change_message_thread_id, find_act, make_admin, create_admins_list, delete_admin
from Buttons import leave_req, choose_form
from Classes import IsAdmin, FSMFillForm


bot = Bot(token='7286065305:AAE9aXpq8R5H0jue4pMVaRijCr5reUQwRQw')
dp = Dispatcher()
maingroupid = -1002472571227
admin_ids: list[int] = [0]
create_table()
create_admins_list(admin_ids)
user_dict: dict[str, str | int | bool] = {}

@dp.message(Command(commands=["help"]), StateFilter(default_state))
async def help_command(message: Message):
    if message.chat.id == maingroupid:
        await bot.send_message(chat_id=message.chat.id, text='Есть такие команды: \n/start - команда, которая начинает'
                                                             '\n/stop - команда, которая завершает ваш диалог с абобусом '
                                                             'общение с ботом \n/MakeMeAdmin - команда, которая делает вас админом '
                                                             '\n/DeleteMeAsAdmin - команда, которая удаляет вас из списка админов ')
    else:
        await bot.send_message(chat_id=message.chat.id, text='Есть такие команды: \n/start - команда, которая начинает'
                                                             '\n/stop - команда, которая завершает ваш диалог с абобусом ')

@dp.message(Command(commands=["MakeMeAdmin"]), StateFilter(default_state))
async def makemeadmin_command(message: Message):
    if message.chat.id == maingroupid:
        make_admin(message.from_user.id)
        admin_ids.append(message.from_user.id)
        await bot.send_message(chat_id=message.from_user.id, text='Вы теперь админ!')
    else:
        await bot.send_message(chat_id=message.from_user.id, text='Вы не являетесь членом профкома!!!')

@dp.message(Command(commands=["DeleteMeASAdmin"]), StateFilter(default_state))
async def deletemeasadmin_command(message: Message):
    if message.chat.id == maingroupid:
        delete_admin(message.from_user.id, admin_ids)
        await bot.send_message(chat_id=message.from_user.id, text='Вы все просрали!!!')
    else:
        await bot.send_message(chat_id=message.from_user.id, text='Вы не являетесь членом профкома!!!')

@dp.message(Command(commands=["start"]), StateFilter(default_state))
async def start_command(message: Message):
    await leave_req(message)

@dp.message(Command(commands=["stop"]), StateFilter(default_state))
async def stop_command(message: Message):

    if message.chat.type != 'private':
        change_act(find_chat_id(message.message_thread_id))
        await bot.send_message(chat_id=find_chat_id(message.message_thread_id), text="Диалог был завершен, если хотите задать новый вопрос, введите /start")

    elif find_act(message.from_user.id) == 1 and message.chat.type == 'private':
        change_act(message.from_user.id)
        await bot.send_message(chat_id=maingroupid, text='Пользователь завершил диалог',
                               message_thread_id=find_group_id(message.from_user.id))
        await bot.send_message(chat_id=message.from_user.id, text='Вы закончили диалог с профкомом,'
                                                                  ' если хотите задать новый вопрос, введите /start')

    elif find_act(message.from_user.id) == 0:
        await bot.send_message(chat_id=message.from_user.id, text='У вас нет активного диалога, '
                                                                  'если вы хотите его начать, введите команду /start')

@dp.callback_query(F.data == "leave_req",StateFilter(default_state))
async def button_check(callback: types.CallbackQuery, state: FSMContext):
    if check_user_id(callback.from_user.id) == True and find_act(callback.from_user.id) == 0:

        change_act(callback.from_user.id)
        await callback.message.answer('Задайте ваш вопрос!')
        await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)

    elif check_user_id(callback.from_user.id) == True and find_act(callback.from_user.id) == 1:

        await callback.message.answer('Задайте ваш вопрос!')
        await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)

    else:

        await callback.message.answer('Введите ваше ФИО')
        await state.set_state(FSMFillForm.FIO)
        await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)

@dp.message(StateFilter(FSMFillForm.FIO),  F.text)
async def process_name_sent(message: Message, state: FSMContext):

    await state.update_data(FIO=message.text)
    await choose_form(message)
    await state.set_state(FSMFillForm.study_form)

@dp.message(StateFilter(FSMFillForm.FIO))
async def warning_not_name(message: Message, state: FSMContext):

    await bot.send_message(text='Это не ФИО, введите ваше ФИО без использования дополнительных символов!', chat_id=message.from_user.id)

@dp.callback_query(StateFilter(FSMFillForm.study_form))
async def process_form_press(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(study_form=callback.data)
    await bot.send_message(
        text='Введите ваш вопрос', chat_id=callback.from_user.id)
    await state.set_state(FSMFillForm.que)

@dp.message(StateFilter(FSMFillForm.study_form))
async def warning_not_button(message: Message, state: FSMContext):
    await bot.send_message(text='Выберите из предложенных варинтов!', chat_id=message.from_user.id)

@dp.message(StateFilter(FSMFillForm.que),  F.text)
async def process_que_sent(message: Message, state: FSMContext):
    create_new_user(message.from_user.id)
    await state.update_data(que=message.text)
    await message.answer(text= 'Диалог начался, если вы хотите '
                               'его закончить, напишите команду /stop. '
                               '\nВы все равно получите сообщение от сотрудника профкома')

    user_dict: dict[int, dict[str, str | int | bool]] = {}
    user_dict[message.from_user.id] = await state.get_data()

    result = await bot.create_forum_topic(chat_id=maingroupid, name=user_dict[message.from_user.id]['FIO'])
    change_message_thread_id(message.from_user.id, result.message_thread_id)
    message_thread_id = find_group_id(message.from_user.id)
    await bot.send_message(text = 'Форма обучения: ' + user_dict[message.from_user.id]['study_form'] + '\nВопрос: '
                                  + user_dict[message.from_user.id]['que'],
                           chat_id=maingroupid, message_thread_id=message_thread_id)
    await state.clear()

@dp.message(StateFilter(FSMFillForm.que))
async def warning_not_que(message: Message, state: FSMContext):
    await bot.send_message(text='Данное сообщение не является вопросом, сначала введите текст вопроса. '
                                'Любую дополнительную информацию '
                                '(например картинка) отправьте следующим сообещнием!', chat_id=message.from_user.id)

@dp.message(IsAdmin(admin_ids), StateFilter(default_state))
async def answer_if_admins_update(message: Message):
    if message.chat.type == 'private':
        await bot.send_message(chat_id=message.from_user.id, text='Ты сам админ из профкома, '
                                                                  'ты зачем вопрос задаешь. Тебе никто не ответит!!!')
    else:

        await message.send_copy(chat_id=find_chat_id(message.message_thread_id))

@dp.message(StateFilter(default_state))
async def send_fio(message: Message):

    if message.chat.id == maingroupid and message.from_user.id != bot.id:
        await bot.send_message(chat_id=message.from_user.id, text='Вы пишите из группы профкома, однако не являетесь '
                                                                  'админом, чтобы им стать, напишите команду '
                                                                  '/MakeMeAdmin в главную группу чата')

    elif find_act(message.from_user.id) == 1 and message.chat.type == 'private':
        message_thread_id = find_group_id(message.from_user.id)
        await message.send_copy(chat_id=maingroupid, message_thread_id=message_thread_id)

    elif find_act(message.from_user.id) == 0 and message.chat.type == 'private':
        await bot.send_message(chat_id=message.from_user.id, text='У вас нет активного диалога, если вы '
                                                                  'хотите его начать, введите команду /start')


if __name__ == '__main__':
    dp.run_polling(bot)

