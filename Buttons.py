from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types


async def leave_req(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Оставить заявку!",
        callback_data="leave_req")
    )
    await message.answer(
        "Вас приветствует бот профкома биофака МГУ \nЗдесь вы можете выбрать один из несокольких вариантов:",
        reply_markup=builder.as_markup()
    )
async def choose_form(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Специалитет",
        callback_data="Специалитет")
    )
    builder.add(types.InlineKeyboardButton(
        text="Бакалавриат",
        callback_data="Бакалавриат")
    )
    builder.add(types.InlineKeyboardButton(
        text="Магистратура",
        callback_data="Магистратура")
    )
    await message.answer(
        "Выберете форму обучения:",
        reply_markup=builder.as_markup()
    )